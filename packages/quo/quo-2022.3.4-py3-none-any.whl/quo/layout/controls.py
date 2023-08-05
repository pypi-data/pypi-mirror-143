"""
User interface Controls for the layout.
"""
import time
from abc import ABCMeta, abstractmethod
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Hashable,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Union,
)

from quo.console.current import get_app
from quo.buffer import Buffer
from quo.cache import SimpleCache
from quo.document import Document
from quo.filters import FilterOrBool, to_filter
from quo.text import (
    AnyFormattedText,
    StyleAndTextTuples,
    to_formatted_text,
)
from quo.text.utils import (
    fragment_list_to_text,
    fragment_list_width,
    split_lines,
)
from quo.highlight import Lexer, SimpleLexer
from quo.mouse_events import MouseEvent, MouseEventType
from quo.search import SearchState
from quo.selection import SelectionType
from quo.utils.utils import get_width as get_cwidth

from .processors import (
    DisplayMultipleCursors,
    HighlightIncrementalSearchProcessor,
    HighlightSearchProcessor,
    HighlightSelectionProcessor,
    Processor,
    TransformationInput,
    merge_processors,
)

if TYPE_CHECKING:
    from quo.keys.key_binding.key_bindings import KeyBindingsBase
    from quo.utils.utils import Event

    # The only two return values for a mouse hander are `None` and
    # `NotImplemented`. For the type checker it's best to annotate this as
    # `object`. (The consumer never expects a more specific instance: checking
    # for NotImplemented can be done using `is NotImplemented`.)
    NotImplementedOrNone = object
    # Other non-working options are:
    # * Optional[Literal[NotImplemented]]
    #      --> Doesn't work, Literal can't take an Any.
    # * None
    #      --> Doesn't work. We can't assign the result of a function that
    #          returns `None` to a variable.
    # * Any
    #      --> Works, but too broad.


__all__ = [
    "BufferControl",
    "SearchBufferControl",
    "DummyControl",
    "FormattedTextControl",
    "UIControl",
    "UIContent",
]

GetLinePrefixCallable = Callable[[int, int], AnyFormattedText]

Point = NamedTuple("Point", [("x", int), ("y", int)])

class UIControl(metaclass=ABCMeta):
    """
    Base class for all user interface controls.
    """

    def reset(self) -> None:
        # Default reset. (Doesn't have to be implemented.)
        pass

    def preferred_width(self, max_available_width: int) -> Optional[int]:
        return None

    def preferred_height(
        self,
        width: int,
        max_available_height: int,
        wrap_lines: bool,
        get_line_prefix: Optional[GetLinePrefixCallable],
    ) -> Optional[int]:
        return None

    def is_focusable(self) -> bool:
        """
        Tell whether this user control is focusable.
        """
        return False

    @abstractmethod
    def create_content(self, width: int, height: int) -> "UIContent":
        """
        Generate the content for this user control.

        Returns a :class:`.UIContent` instance.
        """

    def mouse_handler(self, mouse_event: MouseEvent) -> "NotImplementedOrNone":
        """
        Handle mouse events.

        When `NotImplemented` is returned, it means that the given event is not
        handled by the `UIControl` itself. The `Window` or key bindings can
        decide to handle this event as scrolling or changing focus.

        :param mouse_event: `MouseEvent` instance.
        """
        return NotImplemented

    def move_cursor_down(self) -> None:
        """
        Request to move the cursor down.
        This happens when scrolling down and the cursor is completely at the
        top.
        """

    def move_cursor_up(self) -> None:
        """
        Request to move the cursor up.
        """

    def get_key_bindings(self) -> Optional["KeyBindingsBase"]:
        """
        The key bindings that are specific for this user control.

        Return a :class:`.KeyBinder` object if some key bindings are
        specified, or `None` otherwise.
        """

    def get_invalidate_events(self) -> Iterable["Event[object]"]:
        """
        Return a list of `Event` objects. This can be a generator.
        (The application collects all these events, in order to bind redraw
        handlers to these events.)
        """
        return []


class UIContent:
    """
    Content generated by a user control. This content consists of a list of
    lines.

    :param get_line: Callable that takes a line number and returns the current
        line. This is a list of (style_str, text) tuples.
    :param line_count: The number of lines.
    :param cursor_position: a :class:`.Point` for the cursor position.
    :param menu_position: a :class:`.Point` for the menu position.
    :param show_cursor: Make the cursor visible.
    """

    def __init__(
        self,
        get_line: Callable[[int], StyleAndTextTuples] = (lambda i: []),
        line_count: int = 0,
        cursor_position: Optional[Point] = None,
        menu_position: Optional[Point] = None,
        show_cursor: bool = True,
    ):

        self.get_line = get_line
        self.line_count = line_count
        self.cursor_position = cursor_position or Point(x=0, y=0)
        self.menu_position = menu_position
        self.show_cursor = show_cursor

        # Cache for line heights. Maps cache key -> height
        self._line_heights_cache: Dict[Hashable, int] = {}

    def __getitem__(self, lineno: int) -> StyleAndTextTuples:
        "Make it iterable (iterate line by line)."
        if lineno < self.line_count:
            return self.get_line(lineno)
        else:
            raise IndexError

    def get_height_for_line(
        self,
        lineno: int,
        width: int,
        get_line_prefix: Optional[GetLinePrefixCallable],
        slice_stop: Optional[int] = None,
    ) -> int:
        """
        Return the height that a given line would need if it is rendered in a
        space with the given width (using line wrapping).

        :param get_line_prefix: None or a `Window.get_line_prefix` callable
            that returns the prefix to be inserted before this line.
        :param slice_stop: Wrap only "line[:slice_stop]" and return that
            partial result. This is needed for scrolling the window correctly
            when line wrapping.
        :returns: The computed height.
        """
        # Instead of using `get_line_prefix` as key, we use render_counter
        # instead. This is more reliable, because this function could still be
        # the same, while the content would change over time.
        key = get_app().render_counter, lineno, width, slice_stop

        try:
            return self._line_heights_cache[key]
        except KeyError:
            if width == 0:
                height = 10 ** 8
            else:
                # Calculate line width first.
                line = fragment_list_to_text(self.get_line(lineno))[:slice_stop]
                text_width = get_cwidth(line)

                if get_line_prefix:
                    # Add prefix width.
                    text_width += fragment_list_width(
                        to_formatted_text(get_line_prefix(lineno, 0))
                    )

                    # Slower path: compute path when there's a line prefix.
                    height = 1

                    # Keep wrapping as long as the line doesn't fit.
                    # Keep adding new prefixes for every wrapped line.
                    while text_width > width:
                        height += 1
                        text_width -= width

                        fragments2 = to_formatted_text(
                            get_line_prefix(lineno, height - 1)
                        )
                        prefix_width = get_cwidth(fragment_list_to_text(fragments2))

                        if prefix_width >= width:  # Prefix doesn't fit.
                            height = 10 ** 8
                            break

                        text_width += prefix_width
                else:
                    # Fast path: compute height when there's no line prefix.
                    try:
                        quotient, remainder = divmod(text_width, width)
                    except ZeroDivisionError:
                        height = 10 ** 8
                    else:
                        if remainder:
                            quotient += 1  # Like math.ceil.
                        height = max(1, quotient)

            # Cache and return
            self._line_heights_cache[key] = height
            return height


class FormattedTextControl(UIControl):
    """
    Control that displays formatted text. This can be either plain text, an
    :class:`~quo.text.Text` object, a list of ``(style_str,
    text)`` tuples or a callable that takes no argument and returns one of
    those, depending on how you prefer to do the formatting. See
    ``quo.layout.formatted_text`` for more information.

    (It's mostly optimized for rather small widgets, like toolbars, menus, etc...)

    When this UI control has the focus, the cursor will be shown in the upper
    left corner of this control by default. There are two ways for specifying
    the cursor position:

    - Pass a `get_cursor_position` function which returns a `Point` instance
      with the current cursor position.

    - If the (formatted) text is passed as a list of ``(style, text)`` tuples
      and there is one that looks like ``('[SetCursorPosition]', '')``, then
      this will specify the cursor position.

    Mouse support:

        The list of fragments can also contain tuples of three items, looking like:
        (style_str, text, handler). When mouse support is enabled and the user
        clicks on this fragment, then the given handler is called. That handler
        should accept two inputs: (Application, MouseEvent) and it should
        either handle the event or return `NotImplemented` in case we want the
        containing Window to handle this event.

    :param focusable: `bool` or :class:`.Filter`: Tell whether this control is
        focusable.

    :param text: Text or formatted text to be displayed.
    :param style: Style string applied to the content. (If you want to style
        the whole :class:`~quo.layout.Window`, pass the style to the
        :class:`~quo.layout.Window` instead.)
    :param bind: a :class:`.KeyBinder` object.
    :param get_cursor_position: A callable that returns the cursor position as
        a `Point` instance.
    """

    def __init__(
        self,
        text: AnyFormattedText = "",
        style: str = "",
        focusable: FilterOrBool = False,
        bind: Optional["KeyBindingsBase"] = None,
        show_cursor: bool = True,
        modal: bool = False,
        get_cursor_position: Optional[Callable[[], Optional[Point]]] = None,
    ) -> None:

        self.text = text  # No type check on 'text'. This is done dynamically.
        self.style = style
        self.focusable = to_filter(focusable)

        # Key bindings.
        self.bind = bind
        self.show_cursor = show_cursor
        self.modal = modal
        self.get_cursor_position = get_cursor_position

        #: Cache for the content.
        self._content_cache: SimpleCache[Hashable, UIContent] = SimpleCache(maxsize=18)
        self._fragment_cache: SimpleCache[int, StyleAndTextTuples] = SimpleCache(
            maxsize=1
        )
        # Only cache one fragment list. We don't need the previous item.

        # Render info for the mouse support.
        self._fragments: Optional[StyleAndTextTuples] = None

    def reset(self) -> None:
        self._fragments = None

    def is_focusable(self) -> bool:
        return self.focusable()

    def __repr__(self) -> str:
        return "%s(%r)" % (self.__class__.__name__, self.text)

    def _get_formatted_text_cached(self) -> StyleAndTextTuples:
        """
        Get fragments, but only retrieve fragments once during one render run.
        (This function is called several times during one rendering, because
        we also need those for calculating the dimensions.)
        """
        return self._fragment_cache.get(
            get_app().render_counter, lambda: to_formatted_text(self.text, self.style)
        )

    def preferred_width(self, max_available_width: int) -> int:
        """
        Return the preferred width for this control.
        That is the width of the longest line.
        """
        text = fragment_list_to_text(self._get_formatted_text_cached())
        line_lengths = [get_cwidth(l) for l in text.split("\n")]
        return max(line_lengths)

    def preferred_height(
        self,
        width: int,
        max_available_height: int,
        wrap_lines: bool,
        get_line_prefix: Optional[GetLinePrefixCallable],
    ) -> Optional[int]:
        """
        Return the preferred height for this control.
        """
        content = self.create_content(width, None)
        if wrap_lines:
            height = 0
            for i in range(content.line_count):
                height += content.get_height_for_line(i, width, get_line_prefix)
                if height >= max_available_height:
                    return max_available_height
            return height
        else:
            return content.line_count

    def create_content(self, width: int, height: Optional[int]) -> UIContent:
        # Get fragments
        fragments_with_mouse_handlers = self._get_formatted_text_cached()
        fragment_lines_with_mouse_handlers = list(
            split_lines(fragments_with_mouse_handlers)
        )

        # Strip mouse handlers from fragments.
        fragment_lines: List[StyleAndTextTuples] = [
            [(item[0], item[1]) for item in line]
            for line in fragment_lines_with_mouse_handlers
        ]

        # Keep track of the fragments with mouse handler, for later use in
        # `mouse_handler`.
        self._fragments = fragments_with_mouse_handlers

        # If there is a `[SetCursorPosition]` in the fragment list, set the
        # cursor position here.
        def get_cursor_position(
            fragment: str = "[SetCursorPosition]",
        ) -> Optional[Point]:
            for y, line in enumerate(fragment_lines):
                x = 0
                for style_str, text, *_ in line:
                    if fragment in style_str:
                        return Point(x=x, y=y)
                    x += len(text)
            return None

        # If there is a `[SetMenuPosition]`, set the menu over here.
        def get_menu_position() -> Optional[Point]:
            return get_cursor_position("[SetMenuPosition]")

        cursor_position = (self.get_cursor_position or get_cursor_position)()

        # Create content, or take it from the cache.
        key = (tuple(fragments_with_mouse_handlers), width, cursor_position)

        def get_content() -> UIContent:
            return UIContent(
                get_line=lambda i: fragment_lines[i],
                line_count=len(fragment_lines),
                show_cursor=self.show_cursor,
                cursor_position=cursor_position,
                menu_position=get_menu_position(),
            )

        return self._content_cache.get(key, get_content)

    def mouse_handler(self, mouse_event: MouseEvent) -> "NotImplementedOrNone":
        """
        Handle mouse events.

        (When the fragment list contained mouse handlers and the user clicked on
        on any of these, the matching handler is called. This handler can still
        return `NotImplemented` in case we want the
        :class:`~quo.layout.Window` to handle this particular
        event.)
        """
        if self._fragments:
            # Read the generator.
            fragments_for_line = list(split_lines(self._fragments))

            try:
                fragments = fragments_for_line[mouse_event.position.y]
            except IndexError:
                return NotImplemented
            else:
                # Find position in the fragment list.
                xpos = mouse_event.position.x

                # Find mouse handler for this character.
                count = 0
                for item in fragments:
                    count += len(item[1])
                    if count > xpos:
                        if len(item) >= 3:
                            # Handler found. Call it.
                            # (Handler can return NotImplemented, so return
                            # that result.)
                            handler = item[2]  # type: ignore
                            return handler(mouse_event)
                        else:
                            break

        # Otherwise, don't handle here.
        return NotImplemented

    def is_modal(self) -> bool:
        return self.modal

    def get_key_bindings(self) -> Optional["KeyBindingsBase"]:
        return self.bind


class DummyControl(UIControl):
    """
    A dummy control object that doesn't paint any content.

    Useful for filling a :class:`~quo.layout.Window`. (The
    `fragment` and `char` attributes of the `Window` class can be used to
    define the filling.)
    """

    def create_content(self, width: int, height: int) -> UIContent:
        def get_line(i: int) -> StyleAndTextTuples:
            return []

        return UIContent(
            get_line=get_line, line_count=100 ** 100
        )  # Something very big.

    def is_focusable(self) -> bool:
        return False


_ProcessedLine = NamedTuple(
    "_ProcessedLine",
    [
        ("fragments", StyleAndTextTuples),
        ("source_to_display", Callable[[int], int]),
        ("display_to_source", Callable[[int], int]),
    ],
)


class BufferControl(UIControl):
    """
    Control for visualising the content of a :class:`.Buffer`.

    :param buffer: The :class:`.Buffer` object to be displayed.
    :param input_processors: A list of
        :class:`~quo.layout.processors.Processor` objects.
    :param include_default_input_processors: When True, include the default
        processors for highlighting of selection, search and displaying of
        multiple cursors.
    :param lexer: :class:`.Lexer` instance for syntax highlighting.
    :param preview_search: `bool` or :class:`.Filter`: Show search while
        typing. When this is `True`, probably you want to add a
        ``HighlightIncrementalSearchProcessor`` as well. Otherwise only the
        cursor position will move, but the text won't be highlighted.
    :param focusable: `bool` or :class:`.Filter`: Tell whether this control is focusable.
    :param focus_on_click: Focus this buffer when it's click, but not yet focused.
    :param bind: a :class:`.KeyBinder` object.
    """

    def __init__(
        self,
        buffer: Optional[Buffer] = None,
        input_processors: Optional[List[Processor]] = None,
        include_default_input_processors: bool = True,
        highlighter: Optional[Lexer] = None,
        preview_search: FilterOrBool = False,
        focusable: FilterOrBool = True,
        search_buffer_control: Union[
            None, "SearchBufferControl", Callable[[], "SearchBufferControl"]
        ] = None,
        menu_position: Optional[Callable[[], Optional[int]]] = None,
        focus_on_click: FilterOrBool = False,
        bind: Optional["KeyBindingsBase"] = None,
    ):

        self.input_processors = input_processors
        self.include_default_input_processors = include_default_input_processors

        self.default_input_processors = [
            HighlightSearchProcessor(),
            HighlightIncrementalSearchProcessor(),
            HighlightSelectionProcessor(),
            DisplayMultipleCursors(),
        ]

        self.preview_search = to_filter(preview_search)
        self.focusable = to_filter(focusable)
        self.focus_on_click = to_filter(focus_on_click)

        self.buffer = buffer or Buffer()
        self.menu_position = menu_position
        self.highlighter = highlighter or SimpleLexer()
        self.bind = bind
        self._search_buffer_control = search_buffer_control

        #: Cache for the lexer.
        #: Often, due to cursor movement, undo/redo and window resizing
        #: operations, it happens that a short time, the same document has to be
        #: lexed. This is a fairly easy way to cache such an expensive operation.
        self._fragment_cache: SimpleCache[
            Hashable, Callable[[int], StyleAndTextTuples]
        ] = SimpleCache(maxsize=8)

        self._last_click_timestamp: Optional[float] = None
        self._last_get_processed_line: Optional[Callable[[int], _ProcessedLine]] = None

    def __repr__(self) -> str:
        return "<%s buffer=%r at %r>" % (self.__class__.__name__, self.buffer, id(self))

    @property
    def search_buffer_control(self) -> Optional["SearchBufferControl"]:
        result: Optional[SearchBufferControl]

        if callable(self._search_buffer_control):
            result = self._search_buffer_control()
        else:
            result = self._search_buffer_control

        assert result is None or isinstance(result, SearchBufferControl)
        return result

    @property
    def search_buffer(self) -> Optional[Buffer]:
        control = self.search_buffer_control
        if control is not None:
            return control.buffer
        return None

    @property
    def search_state(self) -> SearchState:
        """
        Return the `SearchState` for searching this `BufferControl`. This is
        always associated with the search control. If one search bar is used
        for searching multiple `BufferControls`, then they share the same
        `SearchState`.
        """
        search_buffer_control = self.search_buffer_control
        if search_buffer_control:
            return search_buffer_control.searcher_search_state
        else:
            return SearchState()

    def is_focusable(self) -> bool:
        return self.focusable()

    def preferred_width(self, max_available_width: int) -> Optional[int]:
        """
        This should return the preferred width.

        Note: We don't specify a preferred width according to the content,
              because it would be too expensive. Calculating the preferred
              width can be done by calculating the longest line, but this would
              require applying all the processors to each line. This is
              unfeasible for a larger document, and doing it for small
              documents only would result in inconsistent behaviour.
        """
        return None

    def preferred_height(
        self,
        width: int,
        max_available_height: int,
        wrap_lines: bool,
        get_line_prefix: Optional[GetLinePrefixCallable],
    ) -> Optional[int]:

        # Calculate the content height, if it was drawn on a screen with the
        # given width.
        height = 0
        content = self.create_content(width, height=1)  # Pass a dummy '1' as height.

        # When line wrapping is off, the height should be equal to the amount
        # of lines.
        if not wrap_lines:
            return content.line_count

        # When the number of lines exceeds the max_available_height, just
        # return max_available_height. No need to calculate anything.
        if content.line_count >= max_available_height:
            return max_available_height

        for i in range(content.line_count):
            height += content.get_height_for_line(i, width, get_line_prefix)

            if height >= max_available_height:
                return max_available_height

        return height

    def _get_formatted_text_for_line_func(
        self, document: Document
    ) -> Callable[[int], StyleAndTextTuples]:
        """
        Create a function that returns the fragments for a given line.
        """
        # Cache using `document.text`.
        def get_formatted_text_for_line() -> Callable[[int], StyleAndTextTuples]:
            return self.highlighter.lex_document(document)

        key = (document.text, self.highlighter.invalidation_hash())
        return self._fragment_cache.get(key, get_formatted_text_for_line)

    def _create_get_processed_line_func(
        self, document: Document, width: int, height: int
    ) -> Callable[[int], _ProcessedLine]:
        """
        Create a function that takes a line number of the current document and
        returns a _ProcessedLine(processed_fragments, source_to_display, display_to_source)
        tuple.
        """
        # Merge all input processors together.
        input_processors = self.input_processors or []
        if self.include_default_input_processors:
            input_processors = self.default_input_processors + input_processors

        merged_processor = merge_processors(input_processors)

        def transform(lineno: int, fragments: StyleAndTextTuples) -> _ProcessedLine:
            "Transform the fragments for a given line number."
            # Get cursor position at this line.
            def source_to_display(i: int) -> int:
                """X position from the buffer to the x position in the
                processed fragment list. By default, we start from the 'identity'
                operation."""
                return i

            transformation = merged_processor.apply_transformation(
                TransformationInput(
                    self, document, lineno, source_to_display, fragments, width, height
                )
            )

            return _ProcessedLine(
                transformation.fragments,
                transformation.source_to_display,
                transformation.display_to_source,
            )

        def create_func() -> Callable[[int], _ProcessedLine]:
            get_line = self._get_formatted_text_for_line_func(document)
            cache: Dict[int, _ProcessedLine] = {}

            def get_processed_line(i: int) -> _ProcessedLine:
                try:
                    return cache[i]
                except KeyError:
                    processed_line = transform(i, get_line(i))
                    cache[i] = processed_line
                    return processed_line

            return get_processed_line

        return create_func()

    def create_content(
        self, width: int, height: int, preview_search: bool = False
    ) -> UIContent:
        """
        Create a UIContent.
        """
        buffer = self.buffer

        # Trigger history loading of the buffer. We do this during the
        # rendering of the UI here, because it needs to happen when an
        # `Application` with its event loop is running. During the rendering of
        # the buffer control is the earliest place we can achieve this, where
        # we're sure the right event loop is active, and don't require user
        # interaction (like in a key binding).
        buffer.load_history_if_not_yet_loaded()

        # Get the document to be shown. If we are currently searching (the
        # search buffer has focus, and the preview_search filter is enabled),
        # then use the search document, which has possibly a different
        # text/cursor position.)
        search_control = self.search_buffer_control
        preview_now = preview_search or bool(
            # Only if this feature is enabled.
            self.preview_search()
            and
            # And something was typed in the associated search field.
            search_control
            and search_control.buffer.text
            and
            # And we are searching in this control. (Many controls can point to
            # the same search field, like in Pyvim.)
            get_app().layout.search_target_buffer_control == self
        )

        if preview_now and search_control is not None:
            ss = self.search_state

            document = buffer.document_for_search(
                SearchState(
                    text=search_control.buffer.text,
                    direction=ss.direction,
                    ignore_case=ss.ignore_case,
                )
            )
        else:
            document = buffer.document

        get_processed_line = self._create_get_processed_line_func(
            document, width, height
        )
        self._last_get_processed_line = get_processed_line

        def translate_rowcol(row: int, col: int) -> Point:
            "Return the content column for this coordinate."
            return Point(x=get_processed_line(row).source_to_display(col), y=row)

        def get_line(i: int) -> StyleAndTextTuples:
            "Return the fragments for a given line number."
            fragments = get_processed_line(i).fragments

            # Add a space at the end, because that is a possible cursor
            # position. (When inserting after the input.) We should do this on
            # all the lines, not just the line containing the cursor. (Because
            # otherwise, line wrapping/scrolling could change when moving the
            # cursor around.)
            fragments = fragments + [("", " ")]
            return fragments

        content = UIContent(
            get_line=get_line,
            line_count=document.line_count,
            cursor_position=translate_rowcol(
                document.cursor_position_row, document.cursor_position_col
            ),
        )

        # If there is an auto completion going on, use that start point for a
        # pop-up menu position. (But only when this buffer has the focus --
        # there is only one place for a menu, determined by the focused buffer.)
        if get_app().layout.current_control == self:
            menu_position = self.menu_position() if self.menu_position else None
            if menu_position is not None:
                assert isinstance(menu_position, int)
                menu_row, menu_col = buffer.document.translate_index_to_position(
                    menu_position
                )
                content.menu_position = translate_rowcol(menu_row, menu_col)
            elif buffer.complete_state:
                # Position for completion menu.
                # Note: We use 'min', because the original cursor position could be
                #       behind the input string when the actual completion is for
                #       some reason shorter than the text we had before. (A completion
                #       can change and shorten the input.)
                menu_row, menu_col = buffer.document.translate_index_to_position(
                    min(
                        buffer.cursor_position,
                        buffer.complete_state.original_document.cursor_position,
                    )
                )
                content.menu_position = translate_rowcol(menu_row, menu_col)
            else:
                content.menu_position = None

        return content

    def mouse_handler(self, mouse_event: MouseEvent) -> "NotImplementedOrNone":
        """
        Mouse handler for this control.
        """
        buffer = self.buffer
        position = mouse_event.position

        # Focus buffer when clicked.
        if get_app().layout.current_control == self:
            if self._last_get_processed_line:
                processed_line = self._last_get_processed_line(position.y)

                # Translate coordinates back to the cursor position of the
                # original input.
                xpos = processed_line.display_to_source(position.x)
                index = buffer.document.translate_row_col_to_index(position.y, xpos)

                # Set the cursor position.
                if mouse_event.event_type == MouseEventType.MOUSE_DOWN:
                    buffer.exit_selection()
                    buffer.cursor_position = index

                elif mouse_event.event_type == MouseEventType.MOUSE_DOWN_MOVE:
                    if buffer.selection_state is None:
                        buffer.start_selection(selection_type=SelectionType.CHARACTERS)
                    buffer.cursor_position = index

                elif mouse_event.event_type == MouseEventType.MOUSE_UP:
                    # When the cursor was moved to another place, select the text.
                    # (The >1 is actually a small but acceptable workaround for
                    # selecting text in Vi navigation mode. In navigation mode,
                    # the cursor can never be after the text, so the cursor
                    # will be repositioned automatically.)
                    if abs(buffer.cursor_position - index) > 1:
                        if buffer.selection_state is None:
                            buffer.start_selection(
                                selection_type=SelectionType.CHARACTERS
                            )
                        buffer.cursor_position = index

                    # Select word around cursor on double click.
                    # Two MOUSE_UP events in a short timespan are considered a double click.
                    double_click = (
                        self._last_click_timestamp
                        and time.time() - self._last_click_timestamp < 0.3
                    )
                    self._last_click_timestamp = time.time()

                    if double_click:
                        start, end = buffer.document.find_boundaries_of_current_word()
                        buffer.cursor_position += start
                        buffer.start_selection(selection_type=SelectionType.CHARACTERS)
                        buffer.cursor_position += end - start
                else:
                    # Don't handle scroll events here.
                    return NotImplemented

        # Not focused, but focusing on click events.
        else:
            if (
                self.focus_on_click()
                and mouse_event.event_type == MouseEventType.MOUSE_UP
            ):
                # Focus happens on mouseup. (If we did this on mousedown, the
                # up event will be received at the point where this widget is
                # focused and be handled anyway.)
                get_app().layout.current_control = self
            else:
                return NotImplemented

        return None

    def move_cursor_down(self) -> None:
        b = self.buffer
        b.cursor_position += b.document.get_cursor_down_position()

    def move_cursor_up(self) -> None:
        b = self.buffer
        b.cursor_position += b.document.get_cursor_up_position()

    def get_key_bindings(self) -> Optional["KeyBindingsBase"]:
        """
        When additional key bindings are given. Return these.
        """
        return self.bind

    def get_invalidate_events(self) -> Iterable["Event[object]"]:
        """
        Return the Window invalidate events.
        """
        # Whenever the buffer changes, the UI has to be updated.
        yield self.buffer.on_text_changed
        yield self.buffer.on_cursor_position_changed

        yield self.buffer.on_completions_changed
        yield self.buffer.on_suggestion_set


class SearchBufferControl(BufferControl):
    """
    :class:`.BufferControl` which is used for searching another
    :class:`.BufferControl`.

    :param ignore_case: Search case insensitive.
    """

    def __init__(
        self,
        buffer: Optional[Buffer] = None,
        input_processors: Optional[List[Processor]] = None,
        highlighter: Optional[Lexer] = None,
        focus_on_click: FilterOrBool = False,
        bind: Optional["KeyBindingsBase"] = None,
        ignore_case: FilterOrBool = False,
    ):

        super().__init__(
            buffer=buffer,
            input_processors=input_processors,
            highlighter=highlighter,
            focus_on_click=focus_on_click,
            bind=bind,
        )

        # If this BufferControl is used as a search field for one or more other
        # BufferControls, then represents the search state.
        self.searcher_search_state = SearchState(ignore_case=ignore_case)
