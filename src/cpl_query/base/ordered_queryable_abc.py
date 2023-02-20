from abc import abstractmethod
from collections.abc import Callable
from typing import Iterable

from cpl_query.base.queryable_abc import QueryableABC


class OrderedQueryableABC(QueryableABC):
    @abstractmethod
    def __init__(self, _t: type, _values: Iterable = None, _func: Callable = None):
        QueryableABC.__init__(self, _t, _values)
        self._funcs: list[Callable] = []
        if _func is not None:
            self._funcs.append(_func)

    @abstractmethod
    def then_by(self, func: Callable) -> "OrderedQueryableABC":
        r"""Sorts OrderedList in ascending order by function

        Parameter:
            func: :class:`Callable`

        Returns:
            list of :class:`cpl_query.iterable.ordered_iterable_abc.OrderedIterableABC`
        """
        pass

    @abstractmethod
    def then_by_descending(self, func: Callable) -> "OrderedQueryableABC":
        r"""Sorts OrderedList in descending order by function

        Parameter:
            func: :class:`Callable`

        Returns:
            list of :class:`cpl_query.iterable.ordered_iterable_abc.OrderedIterableABC`
        """
        pass
