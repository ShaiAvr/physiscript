from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import glfw
from loguru import logger

import physiscript
from physiscript._internal.singleton import Singleton
from physiscript.errors import ApplicationInitializationError

if TYPE_CHECKING:
    from types import TracebackType

__all__ = ["App"]


class App(metaclass=Singleton):
    _width: int
    _height: int
    _title: str
    _vsync: bool

    _window: Any

    def __init__(
        self,
        width: int,
        height: int,
        title: str = "PhysiScript App",
        *,
        vsync: bool = True,
    ) -> None:
        self._width = width
        self._height = height
        self._vsync = vsync

        # TODO: Add GUI logger

        logger.info("physiscript version: {}", physiscript.__version__)
        logger.info("Initializing the application")

        glfw.set_error_callback(type(self)._glfw_error_callback)  # noqa: SLF001
        if not glfw.init():
            raise ApplicationInitializationError("Failed to initialize GLFW")

        glfw.window_hint(glfw.RESIZABLE, False)  # noqa: FBT003
        glfw.window_hint(glfw.DOUBLEBUFFER, True)  # noqa: FBT003
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        logger.trace("GLFW version: {}", glfw.get_version_string().decode())

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
        glfw.terminate()
        logger.success("App was successfully shut down")

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

    @staticmethod
    def _glfw_error_callback(error: int, description: str) -> None:
        logger.error("GLFW error [{}]: {}", error, description)
