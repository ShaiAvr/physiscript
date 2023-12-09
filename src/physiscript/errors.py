__all__ = [
    "SingletonError",
    "PackageInitializationError",
    "ApplicationInitializationError",
    "WindowError",
]


class SingletonError(Exception):
    pass


class PackageInitializationError(Exception):
    pass


class ApplicationInitializationError(Exception):
    pass


class WindowError(Exception):
    pass
