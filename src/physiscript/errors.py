__all__ = ["SingletonError", "PackageInitializationError"]


class SingletonError(Exception):
    pass


class PackageInitializationError(Exception):
    pass
