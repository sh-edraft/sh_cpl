from abc import abstractmethod
from typing import Iterable

from cpl_query.base.queryable_abc import QueryableABC
from cpl_query.base.sequence_abc import SequenceABC
from cpl_query.base.sequence_values import SequenceValues


class IterableABC(SequenceABC, QueryableABC):
    r"""ABC to define functions on list
    """

    @abstractmethod
    def __init__(self, t: type = None, values: Iterable = None):
        SequenceABC.__init__(self, t, values)

    def __getitem__(self, n) -> object:
        return self.to_list().__getitem__(n)

    def __delitem__(self, i: int):
        """Delete an item"""
        _l = self.to_list()
        del _l[i]
        self._values = SequenceValues(_l, self._type)

    def __setitem__(self, i: int, value):
        _l = self.to_list()
        _l.__setitem__(i, value)
        self._values = SequenceValues(_l, self._type)

    def __str__(self):
        return str(self.to_list())

    def append(self, __object: object) -> None:
        r"""Adds element to list
        Parameter
        ---------
            __object: :class:`object`
                value
        """
        if self._type is not None and type(__object) != self._type and not isinstance(type(__object), self._type) and not issubclass(type(__object), self._type):
            raise Exception(f'Unexpected type: {type(__object)}\nExpected type: {self._type}')

        if len(self) == 0 and self._type is None:
            self._type = type(__object)

        self._values = SequenceValues([*self._values, __object], self._type)

    def extend(self, __iterable: Iterable) -> 'IterableABC':
        r"""Adds elements of given list to list
        Parameter
        ---------
            __iterable: :class: `cpl_query.extension.iterable.Iterable`
                index
        """
        for value in __iterable:
            self.append(value)

        return self

    def to_enumerable(self) -> 'EnumerableABC':
        r"""Converts :class: `cpl_query.iterable.iterable_abc.IterableABC` to :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC`

        Returns
        -------
            :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC`
        """
        from cpl_query.enumerable.enumerable import Enumerable
        return Enumerable(self._type, self.to_list())
