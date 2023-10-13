from __future__ import annotations
import os
import re
from importlib.metadata import metadata, PackageNotFoundError
from collections.abc import Iterator
from typing import Final, NamedTuple

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

__all__ = ["App", "HOMEPAGE"]

import loguru
from loguru import logger

_ansi_escape_8bit = re.compile(
    r"\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~]"
)


class _LogEntry(NamedTuple):
    level: int
    message: str
    display_message: str


class _GUILog:
    _logs: list[_LogEntry]

    def __init__(self) -> None:
        self._logs = []

    def __getitem__(self, i: int) -> _LogEntry:
        return self._logs[i]

    def __len__(self) -> int:
        return len(self._logs)

    def __iter__(self) -> Iterator[_LogEntry]:
        return iter(self._logs)

    def clear(self) -> None:
        self._logs.clear()

    def filter(self, min_level: int = 0, filter_: str = "") -> Iterator[_LogEntry]:
        return (e for e in self._logs if e.level >= min_level and filter_ in e.message)

    def add_entry(self, message: loguru.Message) -> None:
        display_message = str(message)
        self._logs.append(
            _LogEntry(
                level=message.record["level"].no,
                message=_ansi_escape_8bit.sub("", display_message),
                display_message=display_message,
            )
        )


_gui_log: Final[_GUILog] = _GUILog()
logger.add(
    _gui_log.add_entry,
    level=0,
    format=(
        "<green>{time:DD.MM.YYYY HH:mm:ss.SSS}</> | "
        "<level>{level: <8}</> | "
        "<cyan>{name}</>:<cyan>{function}</>:<cyan>{line}</> - "
        "<level>{message}</>"
    ),
    colorize=True,
)

HOMEPAGE: str | None

try:
    package_info = metadata("physiscript")
except PackageNotFoundError:
    logger.error(
        "Failed to load package metadata. Make sure the package is installed correctly"
    )
    __version__ = "0.0.0"
    HOMEPAGE = None
else:
    __version__ = package_info["Version"]
    if __version__ is None:
        logger.error("Couldn't retrieve package version")
        __version__ = "0.0.0"
    HOMEPAGE = package_info["Home-page"]
    if HOMEPAGE is None:
        logger.error("Couldn't retrieve package homepage url")
    # No need to keep a reference to the metadata for the entire lifetime of the
    # application
    del package_info

logger.info("physiscript version: {}", __version__)

from physiscript.app import App
