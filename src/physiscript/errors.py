__all__ = [
    "SingletonError",
    "PackageInitializationError",
    "ApplicationInitializationError",
]


class SingletonError(Exception):
    pass


class PackageInitializationError(Exception):
    pass


class ApplicationInitializationError(Exception):
    pass
