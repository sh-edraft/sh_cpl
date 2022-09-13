from abc import abstractmethod
from collections.abc import Callable
from typing import Iterable

from cpl_query.enumerable.enumerable_abc import EnumerableABC


class OrderedEnumerableABC(EnumerableABC):

    @abstractmethod
    def __init__(self, _t: type, _func: Callable = None, _values: Iterable = None):
        EnumerableABC.__init__(self, _t, _values)
        self._funcs: list[Callable] = []
        if _func is not None:
            self._funcs.append(_func)

    @abstractmethod
    def then_by(self, func: Callable) -> 'OrderedEnumerableABC':
        r"""Sorts OrderedList in ascending order by function

        Parameter
        ---------
            func: :class:`Callable`
            
        Returns
        -------
            list of :class:`cpl_query.extension.OrderedEnumerableABC`
        """
        pass

    @abstractmethod
    def then_by_descending(self, func: Callable) -> 'OrderedEnumerableABC':
        r"""Sorts OrderedList in descending order by function

        Parameter
        ---------
            func: :class:`Callable`
            
        Returns
        -------
            list of :class:`cpl_query.extension.OrderedEnumerableABC`
        """
        pass
