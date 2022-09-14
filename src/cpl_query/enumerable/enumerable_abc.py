from abc import abstractmethod
from typing import Iterable

from cpl_query.base.queryable_abc import QueryableABC
from cpl_query.base.sequence_abc import SequenceABC
from cpl_query.base.sequence_values import SequenceValues


class EnumerableABC(SequenceABC, QueryableABC):
    r"""ABC to define functions on list
    """

    @abstractmethod
    def __init__(self, t: type = None, values: Iterable = None):
        SequenceABC.__init__(self, t, values)
        self._remove_error_check = True

    def set_remove_error_check(self, _value: bool):
        r"""Set flag to check if element exists before removing
        """
        self._remove_error_check = _value

    def add(self, __object: object) -> None:
        r"""Adds an element to the enumerable.
        """
        if self._type is not None and type(__object) != self._type and not isinstance(type(__object), self._type) and not issubclass(type(__object), self._type):
            raise Exception(f'Unexpected type: {type(__object)}\nExpected type: {self._type}')

        if len(self) == 0 and self._type is None:
            self._type = type(__object)

        self._values = SequenceValues([*self._values, __object], self._type)

    def clear(self):
        r"""Removes all elements
        """
        del self._values
        self._values = []

    def extend(self, __list: Iterable) -> 'EnumerableABC':
        r"""Adds elements of given list to enumerable

        Parameter
        ---------
            __enumerable: :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC`
                index
        """
        self._values = SequenceValues([*self._values, *__list], self._type)
        return self

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
        self._values = SequenceValues([x for x in self.to_list() if x != __object], self._type)

    def to_iterable(self) -> 'IterableABC':
        r"""Converts :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC` to :class: `cpl_query.iterable.iterable_abc.IterableABC`

        Returns
        -------
            :class: `cpl_query.iterable.iterable_abc.IterableABC`
        """
        from cpl_query.iterable.iterable import Iterable
        return Iterable(self._type, self.to_list())
