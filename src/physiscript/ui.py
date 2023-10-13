from __future__ import annotations
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from enum import Enum, auto
from types import TracebackType
from typing import Any, Self, NamedTuple

import pygame as pg
from imgui.integrations.pygame import PygameRenderer
import imgui

# noinspection PyProtectedMember
from physiscript._internal.singleton import Singleton
from physiscript.utils import Color, ColorLike

__all__ = [
    "UIManager",
    "UIStyle",
    "ColorDisplayMode",
    "AlphaPreviewMode",
    "HuePickerMode",
    "WindowResizeMode",
    "TextInputMode",
    "Condition",
    "BeginEndPair",
    "BeginEndChild",
    "BeginEndMenu",
    "BeginEndMenuBar",
    "BeginEndMainMenuBar",
    "BeginEndPopup",
]


class UIStyle(Enum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> Any:
        return count

    DARK: int = auto()
    LIGHT: int = auto()
    CLASSIC: int = auto()

    def display_name(self) -> str:
        return self.name.capitalize()


_styles_map: dict[UIStyle, Callable[[], None]] = {
    UIStyle.DARK: imgui.style_colors_dark,
    UIStyle.LIGHT: imgui.style_colors_light,
    UIStyle.CLASSIC: imgui.style_colors_classic,
}


class ColorDisplayMode(Enum):
    RGB: int = imgui.COLOR_EDIT_DISPLAY_RGB
    HSV: int = imgui.COLOR_EDIT_DISPLAY_HSV
    HEX: int = imgui.COLOR_EDIT_DISPLAY_HEX


class AlphaPreviewMode(Enum):
    NONE: int = imgui.COLOR_EDIT_NONE
    BACKGROUND: int = imgui.COLOR_EDIT_ALPHA_PREVIEW
    HALF: int = imgui.COLOR_EDIT_ALPHA_PREVIEW_HALF


class HuePickerMode(Enum):
    BAR: int = imgui.COLOR_EDIT_PICKER_HUE_BAR
    WHEEL: int = imgui.COLOR_EDIT_PICKER_HUE_WHEEL


class WindowResizeMode(Enum):
    ALLOW_RESIZE: int = imgui.WINDOW_NONE
    NO_RESIZE: int = imgui.WINDOW_NO_RESIZE
    AUTO_RESIZE: int = imgui.WINDOW_ALWAYS_AUTO_RESIZE


class TextInputMode(Enum):
    DEFAULT: int = imgui.INPUT_TEXT_NONE
    DECIMAL: int = imgui.INPUT_TEXT_CHARS_DECIMAL
    HEX: int = imgui.INPUT_TEXT_CHARS_HEXADECIMAL
    SCIENTIFIC: int = imgui.INPUT_TEXT_CHARS_SCIENTIFIC


class Condition(Enum):
    ALWAYS: int = imgui.ALWAYS
    ONCE: int = imgui.ONCE
    FIRST_USE: int = imgui.FIRST_USE_EVER
    APPEARING: int = imgui.APPEARING


# noinspection PyMethodMayBeStatic
class UIManager(metaclass=Singleton):
    _context: Any
    _impl: PygameRenderer
    _io: Any
    _style: UIStyle

    def __init__(self, width: int, height: int, style: UIStyle = UIStyle.DARK) -> None:
        self._context = imgui.create_context()
        self._impl = PygameRenderer()
        self._io = imgui.get_io()

        # print([name for name in dir(self._io.fonts) if name.startswith("get")])
        # self._io.fonts.add_font_from_file_ttf(
        #     r"D:\Downloads\Assistant\static\Assistant-Regular.ttf",
        #     16,
        #     self._io.fonts.get_glyph_ranges_chinese(),
        # )
        # self._impl.refresh_font_texture()

        self._io.display_size = (width, height)
        self._style = UIStyle.DARK  # Set to default ImGui style
        self.set_style(style)  # Change style if it's different from default

    def begin(
        self,
        label: str,
        *,
        closable: bool = False,
        move: bool = True,
        resize_mode: WindowResizeMode = WindowResizeMode.ALLOW_RESIZE,
        titlebar: bool = True,
        scrollbar: bool = True,
        horizontal_scrollbar: bool = False,
        mouse_scroll: bool = True,
        allow_collapse: bool = True,
        disable_background: bool = False,
        save_settings: bool = True,
        menubar: bool = False,
    ) -> BeginEndPair:
        flags = imgui.WINDOW_NONE
        flags |= (not move) * imgui.WINDOW_NO_MOVE
        flags |= resize_mode.value
        flags |= (not titlebar) * imgui.WINDOW_NO_TITLE_BAR
        flags |= (not scrollbar) * imgui.WINDOW_NO_SCROLLBAR
        flags |= (not mouse_scroll) * imgui.WINDOW_NO_SCROLL_WITH_MOUSE
        flags |= (not allow_collapse) * imgui.WINDOW_NO_COLLAPSE
        flags |= disable_background * imgui.WINDOW_NO_BACKGROUND
        flags |= (not save_settings) * imgui.WINDOW_NO_SAVED_SETTINGS
        flags |= menubar * imgui.WINDOW_MENU_BAR
        flags |= horizontal_scrollbar * imgui.WINDOW_HORIZONTAL_SCROLLING_BAR
        expanded, opened = imgui.begin(label, closable, flags)
        return BeginEndPair(expanded, opened)

    def end(self) -> None:
        imgui.end()

    def begin_child(
        self,
        label: str,
        width: float = 0.0,
        height: float = 0.0,
        *,
        border: bool = False,
        move: bool = True,  # Move main window by dragging child window
        scrollbar: bool = True,
        horizontal_scrollbar: bool = False,
        mouse_scroll: bool = True,
        menubar: bool = False,
    ) -> BeginEndChild:
        flags = imgui.WINDOW_NONE
        flags |= (not move) * imgui.WINDOW_NO_MOVE
        flags |= (not scrollbar) * imgui.WINDOW_NO_SCROLLBAR
        flags |= (not mouse_scroll) * imgui.WINDOW_NO_SCROLL_WITH_MOUSE
        flags |= menubar * imgui.WINDOW_MENU_BAR
        flags |= horizontal_scrollbar * imgui.WINDOW_HORIZONTAL_SCROLLING_BAR
        # noinspection PyArgumentList
        return BeginEndChild(
            imgui.begin_child(label, width, height, border, flags).visible
        )

    def end_child(self) -> None:
        imgui.end_child()

    @property
    def style(self) -> UIStyle:
        return self._style

    def set_style(self, style: UIStyle) -> None:
        if style is self._style:
            return
        self._style = style
        _styles_map[style]()

    def show_user_guide(self) -> None:
        imgui.show_user_guide()

    def imgui_version(self) -> str:
        return imgui.get_version()

    def get_window_width(self) -> float:
        return imgui.get_window_width()

    def get_window_height(self) -> float:
        return imgui.get_window_height()

    def get_window_size(self) -> tuple[float, float]:
        return imgui.get_window_size()

    def get_viewport_work_size(self) -> tuple[float, float]:
        return imgui.get_main_viewport().work_size

    def get_viewport_position(self) -> tuple[float, float]:
        return imgui.get_main_viewport().pos

    def get_viewport_center(self) -> tuple[float, float]:
        return imgui.get_main_viewport().get_center()

    def get_viewport_work_position(self) -> tuple[float, float]:
        return imgui.get_main_viewport().work_pos

    def get_viewport_work_center(self) -> tuple[float, float]:
        return imgui.get_main_viewport().get_work_center()

    def get_viewport_size(self) -> tuple[float, float]:
        return imgui.get_main_viewport().size

    def set_next_window_size(
        self, width: float, height: float, cond: Condition = Condition.ALWAYS
    ) -> None:
        imgui.set_next_window_size(width, height, cond.value)

    def set_next_window_pos(
        self,
        x: float,
        y: float,
        cond: Condition = Condition.ALWAYS,
        pivot_x: float = 0.0,
        pivot_y: float = 0.0,
    ) -> None:
        imgui.set_next_window_position(x, y, cond.value, pivot_x, pivot_y)

    def get_scroll_x(self) -> float:
        return imgui.get_scroll_x()

    def set_scroll_x(self, x: float) -> None:
        imgui.set_scroll_x(x)

    def set_scroll_here_x(self, ratio: float) -> None:
        imgui.set_scroll_here_x(ratio)

    def get_scroll_max_x(self) -> float:
        return imgui.get_scroll_max_x()

    def get_scroll_y(self) -> float:
        return imgui.get_scroll_y()

    def set_scroll_y(self, y: float) -> None:
        imgui.set_scroll_y(y)

    def set_scroll_here_y(self, ratio: float) -> None:
        imgui.set_scroll_here_y(ratio)

    def get_scroll_max_y(self) -> float:
        return imgui.get_scroll_max_y()

    def push_item_width(self, width: float) -> None:
        imgui.push_item_width(width)

    def pop_item_width(self) -> None:
        imgui.pop_item_width()

    @contextmanager
    def item_width(self, width: float) -> Iterator[None]:
        self.push_item_width(width)
        yield
        self.pop_item_width()

    def text(self, text: Any, color: ColorLike | None = None) -> None:
        text = str(text)
        if color is None:
            imgui.text_unformatted(text)
        else:
            color = Color.create(color)
            imgui.text_colored(text, color.red, color.green, color.blue, color.alpha)

    def text_ansi(self, text: Any, color: ColorLike | None = None) -> None:
        text = str(text)
        if color is None:
            imgui.text_ansi(text)
        else:
            color = Color.create(color)
            imgui.text_ansi_colored(text, color.red, color.green, color.blue)

    def bullet_text(self, text: Any) -> None:
        imgui.bullet_text(str(text))

    def disabled_text(self, text: Any) -> None:
        imgui.text_disabled(str(text))

    def wrapped_text(self, text: Any) -> None:
        imgui.text_wrapped(str(text))

    def label_text(self, label: str, text: Any) -> None:
        imgui.label_text(label, str(text))

    def indent(self, width: float = 0.0) -> None:
        imgui.indent(width)

    def unindent(self, width: float = 0.0) -> None:
        imgui.unindent(width)

    @contextmanager
    def indented(self, width: float = 0.0) -> Iterator[None]:
        self.indent(width)
        yield
        self.unindent(width)

    def combo(
        self, label: str, items: list[str], current: int = 0, height: int = -1
    ) -> tuple[bool, int]:
        return imgui.combo(label, current, items, height)

    def color_edit(
        self,
        label: str,
        color: ColorLike,
        *,
        alpha: bool = True,
        display: ColorDisplayMode = ColorDisplayMode.RGB,
        normalized: bool = False,
        alpha_bar: bool = True,
        alpha_preview: AlphaPreviewMode = AlphaPreviewMode.BACKGROUND,
        picker: bool = True,
        hue_picker: HuePickerMode = HuePickerMode.BAR,
        show_label: bool = True,
        show_preview: bool = True,
        tooltip: bool = True,
    ) -> tuple[bool, Color]:
        color = Color.create(color)
        flags = imgui.COLOR_EDIT_DEFAULT_OPTIONS
        # Set display style
        flags &= ~imgui.COLOR_EDIT_DISPLAY_RGB  # Remove default RGB display
        flags |= display.value

        flags |= (not alpha) * imgui.COLOR_EDIT_NO_ALPHA
        flags |= (not picker) * imgui.COLOR_EDIT_NO_PICKER
        flags |= (not tooltip) * imgui.COLOR_EDIT_NO_TOOLTIP
        flags |= normalized * imgui.COLOR_EDIT_FLOAT
        flags |= alpha_bar * imgui.COLOR_EDIT_ALPHA_BAR
        flags |= alpha_preview.value
        # Hue picker
        flags &= ~imgui.COLOR_EDIT_PICKER_HUE_BAR
        flags |= hue_picker.value

        flags |= (not show_label) * imgui.COLOR_EDIT_NO_LABEL
        flags |= (not show_preview) * imgui.COLOR_EDIT_NO_SMALL_PREVIEW

        changed, color = imgui.color_edit4(label, *color.normalized_rgba(), flags)
        return changed, Color(*color)

    def begin_main_menu_bar(self) -> BeginEndMainMenuBar:
        return BeginEndMainMenuBar(imgui.begin_main_menu_bar().opened)

    def end_main_menu_bar(self) -> None:
        imgui.end_main_menu_bar()

    def begin_menu_bar(self) -> BeginEndMenuBar:
        return BeginEndMenuBar(imgui.begin_menu_bar().opened)

    def end_menu_bar(self) -> None:
        imgui.end_menu_bar()

    def begin_menu(self, label: str, enabled: bool = True) -> BeginEndMenu:
        return BeginEndMenu(imgui.begin_menu(label, enabled).opened)

    def end_menu(self) -> None:
        imgui.end_menu()

    def menu_item(
        self,
        label: str,
        shortcut_label: str | None = None,
        selected: bool = False,
        enabled: bool = True,
    ) -> tuple[bool, bool]:
        return imgui.menu_item(label, shortcut_label, selected, enabled)

    def separator(self) -> None:
        imgui.separator()

    def begin_popup(
        self,
        label: str,
        *,
        move: bool = True,
        scrollbar: bool = True,
        mouse_scroll: bool = True,
        disable_background: bool = False,
        menubar: bool = False,
    ) -> BeginEndPopup:
        flags = imgui.WINDOW_NONE
        flags |= (not move) * imgui.WINDOW_NO_MOVE
        flags |= (not scrollbar) * imgui.WINDOW_NO_SCROLLBAR
        flags |= (not mouse_scroll) * imgui.WINDOW_NO_SCROLL_WITH_MOUSE
        flags |= disable_background * imgui.WINDOW_NO_BACKGROUND
        flags |= menubar * imgui.WINDOW_MENU_BAR
        return BeginEndPopup(imgui.begin_popup(label, flags).opened)

    def end_popup(self) -> None:
        imgui.end_popup()

    def open_popup(self, label: str) -> None:
        imgui.open_popup(label)

    def is_popup_open(self, label: str) -> bool:
        return imgui.is_popup_open(label)

    def close_current_popup(self):
        imgui.close_current_popup()

    def begin_popup_modal(
        self,
        label: str,
        move: bool = True,
        resize_mode: WindowResizeMode = WindowResizeMode.ALLOW_RESIZE,
        titlebar: bool = True,
        scrollbar: bool = True,
        horizontal_scrollbar: bool = False,
        mouse_scroll: bool = True,
        disable_background: bool = False,
        save_settings: bool = True,
        menubar: bool = False,
    ) -> BeginEndPopupModal:
        flags = imgui.WINDOW_NONE
        flags |= (not move) * imgui.WINDOW_NO_MOVE
        flags |= resize_mode.value
        flags |= (not titlebar) * imgui.WINDOW_NO_TITLE_BAR
        flags |= (not scrollbar) * imgui.WINDOW_NO_SCROLLBAR
        flags |= (not mouse_scroll) * imgui.WINDOW_NO_SCROLL_WITH_MOUSE
        flags |= disable_background * imgui.WINDOW_NO_BACKGROUND
        flags |= (not save_settings) * imgui.WINDOW_NO_SAVED_SETTINGS
        flags |= menubar * imgui.WINDOW_MENU_BAR
        flags |= horizontal_scrollbar * imgui.WINDOW_HORIZONTAL_SCROLLING_BAR
        # noinspection PyTypeChecker
        res = imgui.begin_popup_modal(label, None, flags)
        return BeginEndPopupModal(res.opened, res.visible)

    def button(self, label: str, width: float = 0, height: float = 0) -> bool:
        return imgui.button(label, width, height)

    def check_box(self, label: str, checked: bool) -> tuple[bool, bool]:
        return imgui.checkbox(label, checked)

    def same_line(self, position: float = 0.0, spacing: float = -1.0) -> None:
        imgui.same_line(position, spacing)

    def text_input(
        self,
        label: str,
        value: str = "",
        hint: str | None = None,
        *,
        length: int = -1,
        password: bool = False,
        mode: TextInputMode = TextInputMode.DEFAULT,
        uppercase: bool = False,
        no_blank: bool = False,
        auto_select: bool = False,
        return_true_on_enter: bool = False,
        allow_tab_input: bool = False,
        read_only: bool = False,
        undo_redo: bool = True,
    ) -> tuple[bool, str]:
        flags = imgui.INPUT_TEXT_NONE
        flags |= password * imgui.INPUT_TEXT_PASSWORD
        flags |= mode.value
        flags |= uppercase * imgui.INPUT_TEXT_CHARS_UPPERCASE
        flags |= no_blank * imgui.INPUT_TEXT_CHARS_NO_BLANK
        flags |= auto_select * imgui.INPUT_TEXT_AUTO_SELECT_ALL
        flags |= return_true_on_enter * imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
        flags |= allow_tab_input * imgui.INPUT_TEXT_ALLOW_TAB_INPUT
        flags |= read_only * imgui.INPUT_TEXT_READ_ONLY
        flags |= (not undo_redo) * imgui.INPUT_TEXT_NO_UNDO_REDO
        if hint is None:
            return imgui.input_text(label, value, length, flags)
        return imgui.input_text_with_hint(label, hint, value, length, flags)

    def multiline_text_input(
        self,
        label: str,
        value: str = "",
        length: int = -1,
        width: float = 0.0,
        height: float = 0.0,
        *,
        password: bool = False,
        mode: TextInputMode = TextInputMode.DEFAULT,
        uppercase: bool = False,
        no_blank: bool = False,
        auto_select: bool = False,
        return_true_on_enter: bool = False,
        allow_tab_input: bool = False,
        read_only: bool = False,
        undo_redo: bool = True,
        ctrl_enter_for_new_line: bool = False,
    ) -> tuple[bool, str]:
        flags = imgui.INPUT_TEXT_NONE
        flags |= password * imgui.INPUT_TEXT_PASSWORD
        flags |= mode.value
        flags |= uppercase * imgui.INPUT_TEXT_CHARS_UPPERCASE
        flags |= no_blank * imgui.INPUT_TEXT_CHARS_NO_BLANK
        flags |= auto_select * imgui.INPUT_TEXT_AUTO_SELECT_ALL
        flags |= return_true_on_enter * imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
        flags |= allow_tab_input * imgui.INPUT_TEXT_ALLOW_TAB_INPUT
        flags |= read_only * imgui.INPUT_TEXT_READ_ONLY
        flags |= (not undo_redo) * imgui.INPUT_TEXT_NO_UNDO_REDO
        flags |= ctrl_enter_for_new_line * imgui.INPUT_TEXT_CTRL_ENTER_FOR_NEW_LINE
        return imgui.input_text_multiline(label, value, length, width, height, flags)

    def next_item_width(self, width: float) -> None:
        imgui.set_next_item_width(width)

    def _shutdown(self) -> None:
        cls = type(self)
        if not cls._remove():
            return
        self._impl.shutdown()
        imgui.destroy_context(self._context)

    def _process_event(self, event: pg.event.Event) -> None:
        self._impl.process_event(event)

    def _process_inputs(self) -> None:
        self._impl.process_inputs()

    def _render(self) -> None:
        imgui.render()
        self._impl.render(imgui.get_draw_data())


class _BeginEndProps(NamedTuple):
    expanded: bool
    opened: bool


class _BeginEndPopupModalProps(NamedTuple):
    opened: bool
    visible: bool


class _BeginEndBase:
    __slots__ = ()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        return False


class _BeginEndWithProps(_BeginEndBase):
    __slots__ = ("_props",)

    _props: tuple[Any, ...]

    def __getitem__(self, i: int) -> Any:
        return self._props[i]

    def __len__(self) -> int:
        return len(self._props)


class BeginEndPair(_BeginEndWithProps):
    __slots__ = ()

    _props: _BeginEndProps

    def __init__(self, expanded: bool, opened: bool) -> None:
        self._props = _BeginEndProps(expanded, opened)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(expanded={self.expanded}, opened={self.opened})"

    @property
    def expanded(self) -> bool:
        return self._props.expanded

    @property
    def opened(self) -> bool:
        return self._props.opened

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        UIManager.get().end()
        return False


class BeginEndChild(_BeginEndBase):
    __slots__ = ("_visible",)

    _visible: bool

    def __init__(self, _visible: bool) -> None:
        self._visible = _visible

    def __repr__(self) -> str:
        return f"{type(self).__name__}(opened={self._visible})"

    def __bool__(self) -> bool:
        return self._visible

    @property
    def visible(self) -> bool:
        return self._visible

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        UIManager.get().end_child()
        return False


class _BeginEndOpenedBase(_BeginEndBase):
    __slots__ = ("_opened",)

    _opened: bool

    def __init__(self, opened: bool) -> None:
        self._opened = opened

    def __repr__(self) -> str:
        return f"{type(self).__name__}(opened={self._opened})"

    def __bool__(self) -> bool:
        return self._opened

    @property
    def opened(self) -> bool:
        return self._opened


class BeginEndPopup(_BeginEndOpenedBase):
    __slots__ = ()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if self._opened:
            UIManager.get().end_popup()
        return False


class BeginEndPopupModal(_BeginEndWithProps):
    __slots__ = ()

    _props: _BeginEndPopupModalProps

    def __init__(self, opened: bool, visible: bool) -> None:
        self._props = _BeginEndPopupModalProps(opened, visible)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(opened={self.opened}, visible={self.visible})"

    @property
    def opened(self) -> bool:
        return self._props.opened

    @property
    def visible(self) -> bool:
        return self._props.visible

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if self.opened:
            UIManager.get().end_popup()
        return False


class BeginEndMenu(_BeginEndOpenedBase):
    __slots__ = ()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if self._opened:
            UIManager.get().end_menu()
        return False


class BeginEndMenuBar(_BeginEndOpenedBase):
    __slots__ = ()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if self._opened:
            UIManager.get().end_menu_bar()
        return False


class BeginEndMainMenuBar(_BeginEndOpenedBase):
    __slots__ = ()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if self._opened:
            UIManager.get().end_main_menu_bar()
        return False
