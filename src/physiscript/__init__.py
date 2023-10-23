from __future__ import annotations
import os
from importlib.metadata import metadata, PackageNotFoundError

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

__all__ = ["App", "HOMEPAGE"]

from physiscript.errors import PackageInitializationError

HOMEPAGE: str | None

try:
    package_info = metadata("physiscript")
except PackageNotFoundError:
    raise PackageInitializationError(
        "Failed to load package metadata. Make sure the package is installed correctly"
    )
else:
    __version__ = package_info["Version"]
    if __version__ is None:
        raise PackageInitializationError("Couldn't retrieve package version")
    HOMEPAGE = package_info["Home-page"]
    if HOMEPAGE is None:
        raise PackageInitializationError("Couldn't retrieve package homepage url")
    # No need to keep a reference to the metadata for the entire lifetime of the
    # application
    del package_info

from physiscript.app import App
