from cpl_core.type import T
from cpl_reactive_extensions.observable import Observable


class Subject(Observable):
    def __init__(self):
        Observable.__init__(self)

        self._value: T = None

    @property
    def value(self) -> T:
        return self._value

    def emit(self, value: T):
        self._value = value
        self._subscriptions()
