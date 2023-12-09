from types import TracebackType
from typing import Any, Self

import glfw
from loguru import logger

from physiscript.errors import WindowError


class Window:
    _window: Any
    _width: int
    _height: int
    _title: str
    _vsync: bool

    def __init__(
        self,
        width: int,
        height: int,
        title: str,
        *,
        vsync: bool = True,
    ) -> None:
        glfw.window_hint(glfw.RESIZABLE, False)  # noqa: FBT003
        glfw.window_hint(glfw.DOUBLEBUFFER, True)  # noqa: FBT003
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self._width = width
        self._height = height
        self._title = title
        self._vsync = vsync

        self._window = glfw.create_window(width, height, title, None, None)
        if not self._window:
            raise WindowError("Failed to create GLFW window")
        self.bind()
        glfw.swap_interval(int(vsync))

    def close(self) -> None:
        logger.info("Closing the window")
        glfw.destroy_window(self._window)
        self._window = None

    def should_close(self) -> bool:
        return glfw.window_should_close(self._window)

    def set_should_close(self, should_close: bool) -> None:  # noqa: FBT001
        glfw.set_window_should_close(self._window, should_close)

    def update(self) -> None:
        glfw.swap_buffers(self._window)
        # Poll events?

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        self.close()
        return False

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def size(self) -> tuple[int, int]:
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

    def bind(self) -> None:
        glfw.make_context_current(self._window)
