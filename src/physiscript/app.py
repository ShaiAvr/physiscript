from __future__ import annotations
from abc import ABC, abstractmethod
from typing import ClassVar
import webbrowser

import imgui
import pygame as pg
import moderngl as mgl
from loguru import logger

import physiscript

# noinspection PyProtectedMember
from physiscript import _gui_log

# noinspection PyProtectedMember
from physiscript._internal.singleton import Singleton
from physiscript.utils import Color, ColorLike, set_clipboard
from physiscript.ui import UIManager, UIStyle, WindowResizeMode, Condition

__all__ = ["App"]


# noinspection PyProtectedMember
class App(metaclass=Singleton):
    _ctx: mgl.Context
    _clock: pg.time.Clock
    _ui: UIManager

    _width: int
    _height: int

    _clear_color: Color
    _fps: int
    _title: str

    running: bool = True
    exit_on_escape: bool
    disable_tools_menubar: bool

    _settings: _SettingsWindow
    _user_guide: _UserGuideWindow
    _about: _AboutWindow
    _log: _LogWindow
    _stats: _StatsWindow

    _FALLBACK_FPS: int = 60

    def __init__(
        self,
        width: int,
        height: int,
        *,
        fps: int | None = None,
        exit_on_escape: bool = True,
        clear_color: ColorLike = "black",
        title: str = "PhysiScript App",
        disable_tools_menubar: bool = False,
    ) -> None:
        self._width = width
        self._height = height
        self.exit_on_escape = exit_on_escape
        self._clear_color = Color.create(clear_color)
        self.disable_tools_menubar = disable_tools_menubar

        logger.info("Initializing the application")
        logger.trace("pygame version: {}", pg.version.ver)
        logger.trace("SDL version: {}", pg.version.SDL)

        success, fails = pg.init()
        logger.trace("pygame.init() - {} modules initialized successfully", success)
        if fails > 0:
            logger.error("pygame.init() - {} modules failed to initialize", fails)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )

        pg.display.set_mode((width, height), flags=pg.OPENGL | pg.DOUBLEBUF)
        try:
            self._ctx = mgl.create_context(require=330)
        except ValueError as e:
            message = f"{e}. Update your graphics drivers."
            logger.critical(message)
            raise ValueError(message)
        self._clock = pg.time.Clock()
        self._ui = UIManager(width, height)
        if fps is None:
            fps = pg.display.get_current_refresh_rate()
            self._fps = fps if fps != 0 else self._FALLBACK_FPS
        else:
            self.fps = fps  # Trigger fps getter for validation
        self.title = title  # Trigger title getter to set window title

        self._settings = _SettingsWindow()
        self._user_guide = _UserGuideWindow()
        self._about = _AboutWindow()
        self._log = _LogWindow()
        self._stats = _StatsWindow()

        logger.success("Application initialized successfully")

        logger.trace("OpenGL info:")
        logger.trace("  Vendor: {info[GL_VENDOR]}", info=self._ctx.info)
        logger.trace("  Renderer: {info[GL_RENDERER]}", info=self._ctx.info)
        logger.trace("  Version: {info[GL_VERSION]}", info=self._ctx.info)

    def shutdown(self) -> None:
        cls = type(self)
        if not cls._remove():
            return
        logger.info("Shutting down the app")
        self._ui._shutdown()
        self._ctx.release()
        pg.quit()
        logger.success("App was successfully shut down")

    def ui(self) -> UIManager:
        return self._ui

    @property
    def screen_width(self) -> int:
        return self._width

    @property
    def screen_height(self) -> int:
        return self._height

    @property
    def fps(self) -> int:
        return self._fps

    @fps.setter
    def fps(self, fps: int) -> None:
        if fps <= 0:
            raise ValueError("FPS must be positive")
        self._fps = fps

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title
        pg.display.set_caption(title)

    @property
    def clear_color(self) -> Color:
        return self._clear_color

    @clear_color.setter
    def clear_color(self, value: ColorLike) -> None:
        self._clear_color = Color.create(value)

    def calculate_fps(self) -> float:
        return self._clock.get_fps()

    def _process_events(self) -> None:
        for ev in pg.event.get():
            if ev.type == pg.QUIT or (
                self.exit_on_escape and ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE
            ):
                self.running = False
            self._ui._process_event(ev)
        self._ui._process_inputs()

    def _on_imgui_render(self) -> None:
        ui = self._ui
        if not self.disable_tools_menubar:
            if ui.begin_main_menu_bar():
                self.main_menu_bar()
                ui.end_main_menu_bar()
        if self._settings.show:
            self._settings.draw()
        if self._log.show:
            self._log.draw()
        if self._user_guide.show:
            self._user_guide.draw()
        if self._about.show:
            self._about.draw()
        if self._stats.show:
            self._stats.draw()

    def main_menu_bar(self) -> None:
        ui = self._ui
        if ui.begin_menu("Tools"):
            _, self._stats.show = ui.menu_item(
                self._stats.title, selected=self._stats.show
            )
            _, self._settings.show = ui.menu_item(
                self._settings.title, selected=self._settings.show
            )
            _, self._log.show = ui.menu_item(self._log.title, selected=self._log.show)
            ui.end_menu()
        if ui.begin_menu("Help"):
            _, self._user_guide.show = ui.menu_item(
                self._user_guide.title, selected=self._user_guide.show
            )
            _, self._about.show = ui.menu_item(
                self._about.title, selected=self._about.show
            )
            ui.end_menu()

    def delta_time(self) -> float:
        return self._clock.get_time()

    def start_frame(self) -> None:
        self._process_events()
        imgui.new_frame()

    def update(self) -> float:
        self._ctx.clear(color=self._clear_color.normalized_rgba())
        # Rendering
        # Render UI
        self._on_imgui_render()
        self._ui._render()
        # Flip screen
        pg.display.flip()
        return self._clock.tick(self._fps)


class _Window(ABC):
    show: bool = False
    resize_mode: WindowResizeMode = WindowResizeMode.ALLOW_RESIZE
    title: ClassVar[str] = "Window"

    def draw(self) -> None:
        ui: UIManager = App.get().ui()
        with ui.begin(
            self.title, closable=True, resize_mode=self.resize_mode
        ) as window:
            self.show = window.opened
            if window.expanded:
                self.render_window()

    @abstractmethod
    def render_window(self) -> None:
        pass


class _SettingsWindow(_Window):
    title: ClassVar[str] = "Settings"
    style_names: ClassVar[list[str]] = [style.display_name() for style in UIStyle]

    def render_window(self) -> None:
        cls = type(self)
        app: App = App.get()
        ui: UIManager = app.ui()
        changed, style = ui.combo("Style", cls.style_names, ui.style.value)
        if changed:
            ui.set_style(UIStyle(style))
        _, app.clear_color = ui.color_edit("Clear Color", app.clear_color, alpha=False)


class _StatsWindow(_Window):
    title: ClassVar[str] = "Stats"
    resize_mode: WindowResizeMode = WindowResizeMode.AUTO_RESIZE

    def render_window(self) -> None:
        app: App = App.get()
        ui: UIManager = app.ui()
        ui.text(
            f"Application average {app.delta_time():.3f} ms "
            f"({app.calculate_fps():.1f} FPS)"
        )


class _UserGuideWindow(_Window):
    title: ClassVar[str] = "User Guide"

    def render_window(self) -> None:
        ui: UIManager = App.get().ui()
        ui.show_user_guide()


class _AboutWindow(_Window):
    title: ClassVar[str] = "About"
    resize_mode: WindowResizeMode = WindowResizeMode.AUTO_RESIZE

    def render_window(self) -> None:
        ui: UIManager = App.get().ui()
        ui.text(f"physiscript {physiscript.__version__}")
        if ui.button("Homepage"):
            if physiscript.HOMEPAGE is None:
                ui.open_popup("Error")
            else:
                webbrowser.open(physiscript.HOMEPAGE)
        ui.separator()
        ui.text(f"Dear ImGui {ui.imgui_version()}")
        ui.text(
            """By Omar Cornut and all Dear ImGui contributors.
Dear ImGui is licensed under the MIT License, see LICENSE for more information.
"""
        )
        if ui.button("ImGui repository"):
            webbrowser.open("https://github.com/ocornut/imgui")
        ui.same_line()
        if ui.button("PyImGui repository"):
            webbrowser.open("https://github.com/pyimgui/pyimgui")
        # Error popup
        x, y = ui.get_viewport_center()
        ui.set_next_window_pos(x, y, Condition.APPEARING, 0.5, 0.5)
        if ui.begin_popup_modal(
            "Error", resize_mode=WindowResizeMode.AUTO_RESIZE
        ).opened:
            ui.text(
                "Couldn't retrieve homepage URL. Make sure the package is "
                "installed correctly"
            )
            if ui.button("Close"):
                ui.close_current_popup()
            ui.end_popup()


class _LogWindow(_Window):
    title: ClassVar[str] = "Log"
    level_names: ClassVar[list[str]] = [
        "Trace",
        "Debug",
        "Info",
        "Success",
        "Warning",
        "Error",
        "Critical",
    ]
    levels: ClassVar[list[int]] = [
        logger.level(name.upper()).no for name in level_names
    ]

    auto_scroll: bool = True
    filter: str = ""
    level_index: int = level_names.index("Info")

    def draw(self) -> None:
        ui: UIManager = App.get().ui()
        ui.set_next_window_size(850, 400, Condition.FIRST_USE)
        super().draw()

    def render_window(self) -> None:
        cls = type(self)
        ui: UIManager = App.get().ui()
        # Options menu
        if ui.begin_popup("Options"):
            _, self.auto_scroll = ui.check_box("Auto-scroll", self.auto_scroll)
            ui.end_popup()

        # Main window
        if ui.button("Options"):
            ui.open_popup("Options")
        ui.same_line()
        if ui.button("Clear"):
            _gui_log.clear()
        ui.same_line()
        if ui.button("Copy"):
            set_clipboard(
                "".join(
                    e.message
                    for e in _gui_log.filter(self.levels[self.level_index], self.filter)
                )
            )
        ui.same_line()
        ui.next_item_width(100)
        _, self.level_index = ui.combo("Level", cls.level_names, self.level_index)
        ui.same_line()
        ui.next_item_width(-100)
        _, self.filter = ui.text_input("Filter", self.filter)
        ui.separator()
        with ui.begin_child("Log", horizontal_scrollbar=True):
            for e in _gui_log.filter(self.levels[self.level_index], self.filter):
                ui.text_ansi(e.display_message)
            if self.auto_scroll and ui.get_scroll_y() >= ui.get_scroll_max_y():
                ui.set_scroll_here_y(1.0)

        # Popups
        x, y = ui.get_viewport_center()
        ui.set_next_window_pos(x, y, Condition.APPEARING, 0.5, 0.5)
        if ui.begin_popup_modal("Demo").opened:
            if ui.button("Close"):
                ui.close_current_popup()
            ui.end_popup()
