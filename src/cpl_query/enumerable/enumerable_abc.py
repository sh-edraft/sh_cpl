from abc import abstractmethod

from cpl_query.base.queryable_abc import QueryableABC


class EnumerableABC(QueryableABC):
    r"""ABC to define functions on list
    """

    @abstractmethod
    def __init__(self, t: type = None, values: list = None):
        QueryableABC.__init__(self, t, values)

        self._remove_error_check = True

    def set_remove_error_check(self, _value: bool):
        r"""Set flag to check if element exists before removing
        """
        self._remove_error_check = _value

    def to_iterable(self) -> 'IterableABC':
        r"""Converts :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC` to :class: `cpl_query.iterable.iterable_abc.IterableABC`

        Returns
        -------
            :class: `cpl_query.iterable.iterable_abc.IterableABC`
        """
        from cpl_query.iterable.iterable import Iterable
        return Iterable(self._type, self.to_list())
