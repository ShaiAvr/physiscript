from __future__ import annotations

from typing import TYPE_CHECKING, Self

import glfw
from loguru import logger

import physiscript
from physiscript.core._singleton import Singleton
from physiscript.core._window import Window
from physiscript.errors import ApplicationInitializationError

if TYPE_CHECKING:
    from types import TracebackType


__all__ = ["App"]


class App(metaclass=Singleton):
    _window: Window

    def __init__(
        self,
        width: int,
        height: int,
        title: str = "PhysiScript App",
        *,
        vsync: bool = True,
    ) -> None:
        # TODO: Add GUI logger

        logger.info("physiscript version: {}", physiscript.__version__)
        logger.info("Initializing the application")

        glfw.set_error_callback(type(self)._glfw_error_callback)  # noqa: SLF001
        if not glfw.init():
            raise ApplicationInitializationError("Failed to initialize GLFW")

        logger.trace("GLFW version: {}", glfw.get_version_string().decode())

        self._window = Window(width, height, title, vsync=vsync)

    def shutdown(self) -> None:
        cls = type(self)
        if not cls._remove():
            return
        logger.info("Shutting down the app")
        self._window.close()
        glfw.terminate()
        logger.success("App was successfully shut down")

    @property
    def running(self) -> bool:
        return not self._window.should_close()

    @running.setter
    def running(self, value: bool) -> None:
        self._window.set_should_close(value)

    def start_frame(self) -> None:
        pass

    def update(self) -> float:
        pass

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
        return self._window.width

    @property
    def screen_height(self) -> int:
        return self._window.height

    @property
    def screen_size(self) -> tuple[int, int]:
        return self._window.size

    @property
    def title(self) -> str:
        return self._window.title

    @title.setter
    def title(self, title: str) -> None:
        self._window.title = title

    @property
    def vsync(self) -> bool:
        return self._window.vsync

    @vsync.setter
    def vsync(self, vsync: bool) -> None:
        self._window.vsync = vsync

    @staticmethod
    def _glfw_error_callback(error: int, description: str) -> None:
        logger.error("GLFW error [{}]: {}", error, description)
