from abc import abstractmethod
from typing import Iterable

from cpl_query.base.queryable_abc import QueryableABC


class IterableABC(QueryableABC):
    r"""ABC to define functions on list"""

    @abstractmethod
    def __init__(self, t: type = None, values: Iterable = None):
        QueryableABC.__init__(self, t, values)

    def __str__(self):
        return str(self.to_list())

    def append(self, _object: object):
        self.add(_object)

    def add(self, _object: object):
        r"""Adds element to list

        Parameter:
            _object: :class:`object`
                value
        """
        self._check_type(_object)
        self._values.append(_object)

    def extend(self, __iterable: Iterable) -> "IterableABC":
        r"""Adds elements of given list to list

        Parameter:
            __iterable: :class: `cpl_query.extension.iterable.Iterable`
                index
        """
        for value in __iterable:
            self.append(value)

        return self

    def remove(self, _object: object):
        r"""Removes element from list

        Parameter:
            _object: :class:`object`
                value
        """
        if _object not in self:
            raise ValueError

        self._values.remove(_object)

    def remove_at(self, _index: int):
        r"""Removes element from list

        Parameter:
            _object: :class:`object`
                value
        """
        self._values.pop(_index)

    def to_enumerable(self) -> "EnumerableABC":
        r"""Converts :class: `cpl_query.iterable.iterable_abc.IterableABC` to :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC`

        Returns:
            :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC`
        """
        from cpl_query.enumerable.enumerable import Enumerable

        return Enumerable(self._type, self.to_list())
