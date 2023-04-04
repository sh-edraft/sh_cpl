from __future__ import annotations

from typing import Optional, Callable, Union, Iterable, Any, TYPE_CHECKING

from cpl_query._helper import is_number
from cpl_query.base import default_lambda

if TYPE_CHECKING:
    from cpl_query.base.ordered_queryable_abc import OrderedQueryableABC
from cpl_query.base.sequence import Sequence
from cpl_query.exceptions import (
    InvalidTypeException,
    ArgumentNoneException,
    ExceptionArgument,
    IndexOutOfRangeException,
)


class QueryableABC(Sequence):
    def __init__(self, t: type, values: Iterable = None):
        Sequence.__init__(self, t, values)

    def all(self, _func: Callable = None) -> bool:
        r"""Checks if every element of list equals result found by function

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            bool
        """
        if _func is None:
            _func = default_lambda

        return self.count(_func) == self.count()

    def any(self, _func: Callable = None) -> bool:
        r"""Checks if list contains result found by function

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            bool
        """
        if _func is None:
            _func = default_lambda

        return self.where(_func).count() > 0

    def average(self, _func: Callable = None) -> Union[int, float, complex]:
        r"""Returns average value of list

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            Union[int, float, complex]
        """
        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        return self.sum(_func) / self.count()

    def contains(self, _value: object) -> bool:
        r"""Checks if list contains value given by function

        Parameter
        ---------
            value: :class:`object`
                value

        Returns
        -------
            bool
        """
        if _value is None:
            raise ArgumentNoneException(ExceptionArgument.value)

        return self.where(lambda x: x == _value).count() > 0

    def count(self, _func: Callable = None) -> int:
        r"""Returns length of list or count of found elements

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            int
        """
        if _func is None:
            return self.__len__()

        return self.where(_func).count()

    def distinct(self, _func: Callable = None) -> QueryableABC:
        r"""Returns list without redundancies

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        if _func is None:
            _func = default_lambda

        result = []
        known_values = []
        for element in self:
            value = _func(element)
            if value in known_values:
                continue

            known_values.append(value)
            result.append(element)

        return type(self)(self._type, result)

    def element_at(self, _index: int) -> any:
        r"""Returns element at given index

        Parameter
        ---------
            _index: :class:`int`
                index

        Returns
        -------
            Value at _index: any
        """
        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        if _index < 0 or _index >= self.count():
            raise IndexOutOfRangeException

        result = self._values[_index]
        if result is None:
            raise IndexOutOfRangeException

        return result

    def element_at_or_default(self, _index: int) -> Optional[any]:
        r"""Returns element at given index or None

        Parameter
        ---------
            _index: :class:`int`
                index

        Returns
        -------
            Value at _index: Optional[any]
        """
        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        try:
            return self._values[_index]
        except IndexError:
            return None

    def first(self) -> any:
        r"""Returns first element

        Returns
        -------
            First element of list: any
        """
        if self.count() == 0:
            raise IndexOutOfRangeException()

        return self._values[0]

    def first_or_default(self) -> any:
        r"""Returns first element or None

        Returns
        -------
            First element of list: Optional[any]
        """
        if self.count() == 0:
            return None

        return self._values[0]

    def for_each(self, _func: Callable = None):
        r"""Runs given function for each element of list

        Parameter
        ---------
            func: :class: `Callable`
                function to call
        """
        if _func is not None:
            for element in self:
                _func(element)

        return self

    def group_by(self, _func: Callable = None) -> QueryableABC:
        r"""Groups by func

        Returns
        -------
            Grouped list[list[any]]: any
        """
        if _func is None:
            _func = default_lambda
        groups = {}

        for v in self:
            value = _func(v)
            if v not in groups:
                groups[value] = []

            groups[value].append(v)

        v = []
        for g in groups.values():
            v.append(type(self)(object, g))
        x = type(self)(type(self), v)
        return x

    def last(self) -> any:
        r"""Returns last element

        Returns
        -------
            Last element of list: any
        """
        if self.count() == 0:
            raise IndexOutOfRangeException()

        return self._values[self.count() - 1]

    def last_or_default(self) -> any:
        r"""Returns last element or None

        Returns
        -------
            Last element of list: Optional[any]
        """
        if self.count() == 0:
            return None

        return self._values[self.count() - 1]

    def max(self, _func: Callable = None) -> object:
        r"""Returns the highest value

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            object
        """
        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        if _func is None:
            _func = default_lambda

        return _func(max(self, key=_func))

    def median(self, _func=None) -> Union[int, float]:
        r"""Return the median value of data elements

        Returns
        -------
            Union[int, float]
        """
        if _func is None:
            _func = default_lambda

        result = self.order_by(_func).select(_func).to_list()
        length = len(result)
        i = int(length / 2)
        return result[i] if length % 2 == 1 else (float(result[i - 1]) + float(result[i])) / float(2)

    def min(self, _func: Callable = None) -> object:
        r"""Returns the lowest value

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            object
        """
        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        if _func is None:
            _func = default_lambda

        return _func(min(self, key=_func))

    def order_by(self, _func: Callable = None) -> OrderedQueryableABC:
        r"""Sorts elements by function in ascending order

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.base.ordered_queryable_abc.OrderedQueryableABC`
        """
        if _func is None:
            _func = default_lambda

        from cpl_query.base.ordered_queryable import OrderedQueryable

        return OrderedQueryable(self.type, sorted(self, key=_func), _func)

    def order_by_descending(self, _func: Callable = None) -> "OrderedQueryableABC":
        r"""Sorts elements by function in descending order

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.base.ordered_queryable_abc.OrderedQueryableABC`
        """
        if _func is None:
            _func = default_lambda

        from cpl_query.base.ordered_queryable import OrderedQueryable

        return OrderedQueryable(self.type, sorted(self, key=_func, reverse=True), _func)

    def reverse(self) -> QueryableABC:
        r"""Reverses list

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        return type(self)(self._type, reversed(self._values))

    def select(self, _func: Callable) -> QueryableABC:
        r"""Formats each element of list to a given format

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        if _func is None:
            _func = default_lambda

        _l = [_func(_o) for _o in self]
        _t = type(_l[0]) if len(_l) > 0 else Any

        return type(self)(_t, _l)

    def select_many(self, _func: Callable) -> QueryableABC:
        r"""Flattens resulting lists to one

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        # The line below is pain. I don't understand anything of it...
        # written on 09.11.2022 by Sven Heidemann
        return type(self)(object, [_a for _o in self for _a in _func(_o)])

    def single(self) -> any:
        r"""Returns one single element of list

        Returns
        -------
            Found value: any

        Raises
        ------
            ArgumentNoneException: when argument is None
            Exception: when argument is None or found more than one element
        """
        if self.count() > 1:
            raise Exception("Found more than one element")
        elif self.count() == 0:
            raise Exception("Found no element")

        return self._values[0]

    def single_or_default(self) -> Optional[any]:
        r"""Returns one single element of list

        Returns
        -------
            Found value: Optional[any]
        """
        if self.count() > 1:
            raise Exception("Index out of range")
        elif self.count() == 0:
            return None

        return self._values[0]

    def skip(self, _index: int) -> QueryableABC:
        r"""Skips all elements from index

        Parameter
        ---------
            _index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        return type(self)(self.type, self._values[_index:])

    def skip_last(self, _index: int) -> QueryableABC:
        r"""Skips all elements after index

        Parameter
        ---------
            _index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        index = self.count() - _index
        return type(self)(self._type, self._values[:index])

    def sum(self, _func: Callable = None) -> Union[int, float, complex]:
        r"""Sum of all values

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            Union[int, float, complex]
        """
        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        if _func is None:
            _func = default_lambda

        result = 0
        for x in self:
            result += _func(x)

        return result

    def split(self, _func: Callable) -> QueryableABC:
        r"""Splits the list by given function


        Parameter
        ---------
            func: :class:`Callable`
                seperator

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        groups = []
        group = []
        for x in self:
            v = _func(x)
            if x == v:
                groups.append(group)
                group = []

            group.append(x)

        groups.append(group)

        query_groups = []
        for g in groups:
            if len(g) == 0:
                continue
            query_groups.append(type(self)(self._type, g))

        return type(self)(self._type, query_groups)

    def take(self, _index: int) -> QueryableABC:
        r"""Takes all elements from index

        Parameter
        ---------
            _index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        return type(self)(self._type, self._values[:_index])

    def take_last(self, _index: int) -> QueryableABC:
        r"""Takes all elements after index

        Parameter
        ---------
            _index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        index = self.count() - _index

        if index >= self.count() or index < 0:
            raise IndexOutOfRangeException()

        return type(self)(self._type, self._values[index:])

    def where(self, _func: Callable = None) -> QueryableABC:
        r"""Select element by function

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        if _func is None:
            _func = default_lambda

        return type(self)(self.type, filter(_func, self))
