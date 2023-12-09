# ruff: noqa: ANN204, ANN002, ANN003, ANN202
from loguru import logger

from physiscript.errors import SingletonError

__all__ = ["Singleton"]


# TODO: Add proper type hints
class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
            return cls._instance
        name = cls.__name__
        message = (
            f"{name} already created. use {name}.get() to get the {name} instance."
        )
        with logger.catch(message=message, reraise=True):
            raise SingletonError(message)

    def get(cls):
        return cls._instance

    def _remove(cls) -> bool:
        res = cls._instance is not None
        cls._instance = None
        return res
