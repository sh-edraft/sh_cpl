from cpl_core.type import T
from cpl_reactive_extensions.observable import Observable


class Subject(Observable):
    def __init__(self, _t: type):
        Observable.__init__(self)

        self._t = _t
        self._value: T = None

    @property
    def value(self) -> T:
        return self._value

    def next(self, value: T):
        if not isinstance(value, self._t):
            raise TypeError(f"Expected {self._t.__name__} not {type(value).__name__}")

        self._value = value
