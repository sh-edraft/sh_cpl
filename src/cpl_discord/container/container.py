from abc import abstractmethod
from typing import Callable


class Container:
    def __init__(self, _o: object, _t: type):
        self._object = _o
        self._type = _t

    def __to_type(_f: Callable, _t: type):
        def wrapper(*args, **kwargs):
            result = _f(*args, **kwargs)
            return _t(result)

        return wrapper

    def __getitem__(self, item):
        result = self._object[item]
        if isinstance(result, type(self._guild)):
            result = self._type(result)
        return result

    def __getattr__(self, item):
        result = getattr(self._object, item)
        if callable(result):
            result = self.__to_type(result, self._type)
        return result

    def __repr__(self):
        return repr(self._object)
