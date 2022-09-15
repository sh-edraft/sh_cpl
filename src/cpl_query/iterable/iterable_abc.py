from abc import abstractmethod
from typing import Iterable

from cpl_query.base.queryable_abc import QueryableABC


class IterableABC(list, QueryableABC):
    r"""ABC to define functions on list
    """

    @abstractmethod
    def __init__(self, t: type = None, values: Iterable = None):
        self._type = t
        list.__init__(self, [] if values is None else values)

    def __repr__(self):
        return f'<{type(self).__name__} {list(self).__repr__()}>'

    @property
    def type(self) -> type:
        return self._type

    def to_list(self) -> list:
        r"""Converts :class: `cpl_query.base.sequence_abc.SequenceABC` to :class: `list`

        Returns
        -------
            :class: `list`
        """
        return [x for x in self]

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

        # self._values = SequenceValues([*self._values, __object], self._type)
        super().append(__object)

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
