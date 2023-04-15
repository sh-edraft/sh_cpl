from cpl_core.type import T
from cpl_reactive_extensions.observable import Observable


class Subject(Observable):
    def __init__(self, _t: type):
        Observable.__init__(self)

        self._t = _t
