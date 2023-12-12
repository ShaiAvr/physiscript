from __future__ import annotations

import platform
from time import sleep
from typing import TYPE_CHECKING, Any, Self

import glfw
from loguru import logger

import physiscript
from physiscript.core._singleton import Singleton
from physiscript.errors import ApplicationInitializationError

if TYPE_CHECKING:
    from types import TracebackType


__all__ = ["App"]


class App(metaclass=Singleton):
    _window: Any
    _width: int
    _height: int
    _title: str
    _vsync: bool

    limit_fps: bool
    _target_fps: int
    enable_idling: bool
    _fps_idle: int
    _is_idling: bool = False

    _frame_start: float

    def __init__(  # noqa: PLR0913
        self,
        width: int,
        height: int,
        title: str = "PhysiScript App",
        *,
        vsync: bool = True,
        limit_fps: bool = False,
        target_fps: int = 60,
        enable_idling: bool = False,
        fps_idle: int = 10,
    ) -> None:
        # TODO: Add GUI logger

        logger.info("physiscript version: {}", physiscript.__version__)
        logger.info("Initializing the application")

        glfw.set_error_callback(type(self)._glfw_error_callback)  # noqa: SLF001
        if not glfw.init():
            raise ApplicationInitializationError("Failed to initialize GLFW")

        logger.trace("GLFW version: {}", glfw.get_version_string().decode())

        glfw.window_hint(glfw.RESIZABLE, False)  # noqa: FBT003
        glfw.window_hint(glfw.DOUBLEBUFFER, True)  # noqa: FBT003
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        if platform.system() == "Darwin":
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)  # noqa: FBT003

        self._width = width
        self._height = height
        self._title = title
        self._vsync = vsync
        self.limit_fps = limit_fps
        self.target_fps = target_fps
        self.enable_idling = enable_idling
        self.fps_idle = fps_idle

        self._window = glfw.create_window(width, height, title, None, None)
        if not self._window:
            raise ApplicationInitializationError("Failed to create GLFW window")
        glfw.make_context_current(self._window)
        glfw.swap_interval(int(vsync))

    def shutdown(self) -> None:
        cls = type(self)
        if not cls._remove():
            return
        logger.info("Shutting down the app")
        glfw.destroy_window(self._window)
        self._window = None
        glfw.terminate()
        logger.success("App was successfully shut down")

    @property
    def running(self) -> bool:
        return not glfw.window_should_close(self._window)

    @running.setter
    def running(self, value: bool) -> None:
        glfw.set_window_should_close(self._window, value)

    def start_frame(self) -> None:
        self._frame_start = glfw.get_time()

    def update(self) -> float:
        glfw.swap_buffers(self._window)
        self._is_idling = False
        poll_events = True
        if self.enable_idling:
            wait_timeout = 1 / self._fps_idle
            before_time = glfw.get_time()
            glfw.wait_events_timeout(wait_timeout)
            poll_events = False
            after_time = glfw.get_time()
            wait_duration = after_time - before_time
            self._is_idling = wait_duration > wait_timeout * 0.9
        if self.limit_fps:
            now = glfw.get_time()
            frame_duration = now - self._frame_start
            timeout = 1 / self._target_fps - frame_duration
            if timeout > 0:
                sleep(timeout)
        if poll_events:
            glfw.poll_events()
        frame_end = glfw.get_time()
        return frame_end - self._frame_start

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        self.shutdown()
        return False

    @property
    def screen_width(self) -> int:
        return self._width

    @property
    def screen_height(self) -> int:
        return self._height

    @property
    def screen_size(self) -> tuple[int, int]:
        return (self._width, self._height)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title
        glfw.set_window_title(self._window, title)

    @property
    def vsync(self) -> bool:
        return self._vsync

    @vsync.setter
    def vsync(self, vsync: bool) -> None:
        self._vsync = vsync
        glfw.swap_interval(int(vsync))

    @property
    def target_fps(self) -> int:
        return self._target_fps

    @target_fps.setter
    def target_fps(self, fps: int) -> None:
        if fps <= 0:
            raise ValueError("FPS must be positive")
        self._target_fps = fps

    @property
    def fps_idle(self) -> int:
        return self._fps_idle

    @fps_idle.setter
    def fps_idle(self, fps: int) -> None:
        if fps <= 0:
            raise ValueError("FPS must be positive")
        self._fps_idle = fps

    @property
    def is_idling(self) -> bool:
        return self._is_idling

    @staticmethod
    def _glfw_error_callback(error: int, description: str) -> None:
        logger.error("GLFW error [{}]: {}", error, description.decode())
