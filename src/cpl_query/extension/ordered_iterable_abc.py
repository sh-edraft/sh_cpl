from abc import abstractmethod
from collections import Callable

from cpl_query.extension.iterable_abc import IterableABC


class OrderedIterableABC(IterableABC):

    @abstractmethod
    def __init__(self, _func: Callable = None):
        IterableABC.__init__(self)
        self._funcs: list[Callable] = []
        if _func is not None:
            self._funcs.append(_func)

    @abstractmethod
    def then_by(self, func: Callable) -> 'OrderedIterableABC': pass

    @abstractmethod
    def then_by_descending(self, func: Callable) -> 'OrderedIterableABC': pass
