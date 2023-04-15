from cpl_core.type import T
from cpl_reactive_extensions.subject import Subject


class BehaviorSubject(Subject):
    def __init__(self, _t: type, value: T):
        Subject.__init__(self, _t)

        if not isinstance(value, _t):
            raise TypeError(f"Expected {_t.__name__} not {type(value).__name__}")

        self._t = _t
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    def next(self, value: T):
        super().next(value)

        self._value = value
