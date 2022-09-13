from abc import ABC, abstractmethod
from typing import Optional, Callable, Union, Iterable

from cpl_query.base.queryable_abc import QueryableABC
from cpl_query.enumerable.enumerable_abc import EnumerableABC


class IterableABC(QueryableABC, list):
    r"""ABC to define functions on list
    """

    @abstractmethod
    def __init__(self, t: type = None, values: list = None):
        list.__init__(self)

        if t == any:
            t = None
        self._type = t

        if values is not None:
            for value in values:
                self.append(value)

    @property
    def type(self) -> type:
        return self._type

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

    def to_list(self) -> list:
        r"""Converts :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC` to :class: `list`

        Returns
        -------
            :class: `list`
        """
        return list(self)
