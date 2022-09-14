from abc import abstractmethod
from typing import Iterable

from cpl_query.base.queryable_abc import QueryableABC
from cpl_query.base.sequence_abc import SequenceABC
from cpl_query.base.sequence_values import SequenceValues


class IterableABC(SequenceABC, QueryableABC):
    r"""ABC to define functions on list
    """

    @abstractmethod
    def __init__(self, t: type = None, values: list = None):
        SequenceABC.__init__(self, t, values)

    def __getitem__(self, n) -> object:
        r"""Gets item in enumerable at specified zero-based index

        Parameter
        --------
            n: the index of the item to get

        Returns
        -------
            The element at the specified index.

        Raises
        ------
            IndexError if n > number of elements in the iterable
        """
        return list.__getitem__(self.to_list(), n)

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
