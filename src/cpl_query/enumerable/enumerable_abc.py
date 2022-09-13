import itertools
from abc import abstractmethod
from typing import Union

from cpl_query.enumerable.enumerable_values import EnumerableValues


class EnumerableABC:

    @abstractmethod
    def __init__(self, t: type = None, values: Union[list, iter] = None):
        if t == any:
            t = None
        self._type = t

        self._values = EnumerableValues(values)
        self._remove_error_check = True

    def set_remove_error_check(self, _value: bool):
        r"""Set flag to check if element exists before removing
        """
        self._remove_error_check = _value

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def next(self):
        return next(self._values)

    def __next__(self):
        return self.next()

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
        for i, e in enumerate(self):
            if i == n:
                return e

    def __repr__(self):
        return f'<EnumerableABC {list(self).__repr__()}>'

    @property
    def type(self) -> type:
        return self._type

    def add(self, __object: object) -> None:
        r"""Adds an element to the enumerable.
        """
        if self._type is not None and type(__object) != self._type and not isinstance(type(__object), self._type) and not issubclass(type(__object), self._type):
            raise Exception(f'Unexpected type: {type(__object)}\nExpected type: {self._type}')

        if len(self) == 0 and self._type is None:
            self._type = type(__object)

        self._values = EnumerableValues([*self._values, __object])

    def count(self) -> int:
        r"""Returns count of  elements

        Returns
        -------
            int
        """
        return sum(1 for element in self)

    def clear(self):
        r"""Removes all elements
        """
        del self._values
        self._values = []

    @staticmethod
    def empty():
        r"""Returns an empty enumerable

        Returns
        -------
            Enumerable object that contains no elements
        """
        return EnumerableABC()

    @staticmethod
    def range(start: int, length: int) -> 'EnumerableABC':
        return EnumerableABC(int, range(start, start + length, 1))

    def remove(self, __object: object) -> None:
        r"""Removes element from list

        Parameter
        ---------
            __object: :class:`object`
                value

        Raises
        ---------
            `Element not found` when element does not exist. Check can be deactivated by calling <enumerable>.set_remove_error_check(False)
        """
        if self._remove_error_check and __object not in self._values:
            raise Exception('Element not found')

        # self._values.remove(__object)
        self._values = EnumerableValues([x for x in self.to_list() if x != __object])

    def to_list(self) -> list:
        r"""Converts :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC` to :class: `list`

        Returns
        -------
            :class: `list`
        """
        return [x for x in self]
