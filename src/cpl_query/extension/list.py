from typing import Iterable as IterableType

from cpl_query.iterable.iterable import Iterable


class List(Iterable, list):
    r"""Implementation of :class: `cpl_query.extension.iterable.Iterable`
    """

    def __init__(self, t: type = None, values: IterableType = None):
        Iterable.__init__(self, t, values)
        list.__init__(self)

    def to_enumerable(self) -> 'EnumerableABC':
        r"""Converts :class: `cpl_query.iterable.iterable_abc.IterableABC` to :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC`

        Returns
        -------
            :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC`
        """
        from cpl_query.enumerable.enumerable import Enumerable
        return Enumerable(self._type, self.to_list())

    def to_iterable(self) -> 'IterableABC':
        r"""Converts :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC` to :class: `cpl_query.iterable.iterable_abc.IterableABC`

        Returns
        -------
            :class: `cpl_query.iterable.iterable_abc.IterableABC`
        """
        from cpl_query.iterable.iterable import Iterable
        return Iterable(self._type, self.to_list())
