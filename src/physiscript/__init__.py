from __future__ import annotations

import os
from importlib.metadata import PackageMetadata, PackageNotFoundError, metadata

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

__all__ = ["App", "HOMEPAGE", "REPOSITORY"]

from physiscript.errors import PackageInitializationError

HOMEPAGE: str
"""URL to the project's homepage (currently the same as :py:data:`REPOSITORY`)."""
REPOSITORY: str
"""URL to the project's repository."""


def _get_homepage(info: PackageMetadata) -> str | None:
    # First try `Home-page`
    homepage = info["Home-page"]
    if homepage is not None:
        return homepage
    # Try `Project-URL` Homepage or Repository
    project_urls = dict(u.split(", ", 1) for u in info.get_all("Project-URL"))
    return project_urls.get("Homepage") or project_urls.get("Repository")


try:
    package_info = metadata("physiscript")
except PackageNotFoundError as e:
    raise PackageInitializationError(
        "Failed to load package metadata. Make sure the package is installed correctly"
    ) from e
else:
    __version__ = package_info["Version"]
    if __version__ is None:
        raise PackageInitializationError("Couldn't retrieve package version")
    __version__ = __version__.removesuffix("+editable")
    HOMEPAGE = _get_homepage(package_info)
    REPOSITORY = HOMEPAGE  # Homepage is repository for now
    if HOMEPAGE is None:
        raise PackageInitializationError("Couldn't retrieve package homepage url")
    # No need to keep a reference to the metadata for the entire lifetime of the
    # application
    del package_info

from physiscript.app import App
