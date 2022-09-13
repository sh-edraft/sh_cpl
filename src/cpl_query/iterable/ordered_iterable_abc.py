from abc import abstractmethod
from collections.abc import Callable

from cpl_query.iterable.iterable_abc import IterableABC


class OrderedIterableABC(IterableABC):

    @abstractmethod
    def __init__(self, _t: type, _func: Callable = None):
        IterableABC.__init__(self, _t)
        self._funcs: list[Callable] = []
        if _func is not None:
            self._funcs.append(_func)

    @abstractmethod
    def then_by(self, func: Callable) -> 'OrderedIterableABC':
        r"""Sorts OrderedList in ascending order by function

        Parameter
        ---------
            func: :class:`Callable`
            
        Returns
        -------
            list of :class:`cpl_query.extension.OrderedIterableABC`
        """
        pass

    @abstractmethod
    def then_by_descending(self, func: Callable) -> 'OrderedIterableABC':
        r"""Sorts OrderedList in descending order by function

        Parameter
        ---------
            func: :class:`Callable`
            
        Returns
        -------
            list of :class:`cpl_query.extension.OrderedIterableABC`
        """
        pass
