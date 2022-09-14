from typing import Union, Callable, Optional

from cpl_query._helper import is_number
from cpl_query.enumerable.enumerable_abc import EnumerableABC
from cpl_query.enumerable.ordered_enumerable_abc import OrderedEnumerableABC
from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument, InvalidTypeException, IndexOutOfRangeException


def _default_lambda(x: object):
    return x


class Enumerable(EnumerableABC):
    r"""Implementation of :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC`
    """

    def __init__(self, t: type = None, values: Union[list, iter] = None):
        EnumerableABC.__init__(self, t, values)

    def all(self, _func: Callable = None) -> bool:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            _func = _default_lambda

        result = self.where(_func)
        return len(result) == len(self)

    def any(self, _func: Callable = None) -> bool:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            _func = _default_lambda

        result = self.where(_func)
        return len(result) > 0

    def average(self, _func: Callable = None) -> Union[int, float, complex]:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        if _func is None:
            _func = _default_lambda

        return float(self.sum(_func)) / float(self.count())

    def contains(self, _value: object) -> bool:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _value is None:
            raise ArgumentNoneException(ExceptionArgument.value)

        return self.where(lambda x: x == _value).count() > 0

    def count(self, _func: Callable = None) -> int:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            return len(self)

        return len(self.where(_func))

    def distinct(self, _func: Callable = None) -> EnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            _func = _default_lambda

        result = Enumerable()
        known_values = []
        for element in self:
            value = _func(element)
            if value in known_values:
                continue

            known_values.append(value)
            result.add(element)

        return result

    def element_at(self, _index: int) -> any:
        self._values.reset()
        while _index >= 0:
            current = self.next()
            if _index == 0:
                return current
            _index -= 1

    def element_at_or_default(self, _index: int) -> any:
        try:
            return self.element_at(_index)
        except IndexOutOfRangeException:
            return None

    @staticmethod
    def empty() -> 'EnumerableABC':
        r"""Returns an empty enumerable

        Returns
        -------
            Enumerable object that contains no elements
        """
        return Enumerable()

    def first(self: EnumerableABC, _func=None) -> any:
        if _func is not None:
            return self.where(_func).element_at(0)
        return self.element_at(0)

    def first_or_default(self: EnumerableABC, _func=None) -> Optional[any]:
        if _func is not None:
            return self.where(_func).element_at_or_default(0)
        return self.element_at_or_default(0)

    def for_each(self, _func: Callable = None):
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            _func = _default_lambda

        for element in self:
            _func(element)

    def last(self: EnumerableABC) -> any:
        return self.element_at(self.count() - 1)

    def last_or_default(self: EnumerableABC) -> Optional[any]:
        return self.element_at_or_default(self.count() - 1)

    def max(self, _func: Callable = None) -> Union[int, float, complex]:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        if _func is None:
            _func = _default_lambda

        return _func(max(self, key=_func))

    def median(self, _func=None) -> Union[int, float]:
        if _func is None:
            _func = _default_lambda
        result = self.order_by(_func).select(_func).to_list()
        length = len(result)
        i = int(length / 2)
        return (
            result[i]
            if length % 2 == 1
            else (float(result[i - 1]) + float(result[i])) / float(2)
        )

    def min(self, _func: Callable = None) -> Union[int, float, complex]:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        if _func is None:
            _func = _default_lambda

        return _func(min(self, key=_func))

    def order_by(self, _func: Callable = None) -> OrderedEnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            _func = _default_lambda

        from cpl_query.enumerable.ordered_enumerable import OrderedEnumerable
        return OrderedEnumerable(self.type, _func, sorted(self, key=_func))

    def order_by_descending(self, _func: Callable = None) -> OrderedEnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            _func = _default_lambda

        from cpl_query.enumerable.ordered_enumerable import OrderedEnumerable
        return OrderedEnumerable(self.type, _func, sorted(self, key=_func, reverse=True))

    @staticmethod
    def range(start: int, length: int) -> 'EnumerableABC':
        return Enumerable(int, range(start, length))

    def reverse(self: EnumerableABC) -> EnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        return Enumerable(self.type, list(reversed(self.to_list())))

    def select(self, _func: Callable = None) -> EnumerableABC:
        if _func is None:
            _func = _default_lambda

        result = Enumerable()
        result.extend(_func(_o) for _o in self)
        return result

    def select_many(self, _func: Callable = None) -> EnumerableABC:
        if _func is None:
            _func = _default_lambda

        result = Enumerable()
        # The line below is pain. I don't understand anything of it...
        # written on 09.11.2022 by Sven Heidemann
        elements = [_a for _o in self for _a in _func(_o)]

        result.extend(elements)
        return result

    def single(self: EnumerableABC) -> any:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(self) > 1:
            raise IndexError('Found more than one element')
        elif len(self) == 0:
            raise IndexOutOfRangeException(f'{type(self).__name__} is empty')

        return self.element_at(0)

    def single_or_default(self: EnumerableABC) -> Optional[any]:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(self) > 1:
            raise IndexError('Found more than one element')
        elif len(self) == 0:
            return None

        return self.element_at(0)

    def skip(self, _index: int) -> EnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        _list = self.to_list()

        if _index >= len(_list):
            raise IndexOutOfRangeException()

        return Enumerable(self.type, _list[_index:])

    def skip_last(self, _index: int) -> EnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        index = len(self) - _index

        if index >= len(self) or index < 0:
            raise IndexOutOfRangeException()

        return self.take(len(self) - _index)

    def take(self, _index: int) -> EnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        _list = self.to_list()

        if _index >= len(_list):
            raise IndexOutOfRangeException()

        return Enumerable(self.type, _list[:_index])

    def take_last(self, _index: int) -> EnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        _list = self.to_list()
        index = len(_list) - _index

        if index >= len(_list) or index < 0:
            raise IndexOutOfRangeException()

        return self.skip(index)

    def sum(self, _func: Callable = None) -> Union[int, float, complex]:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        if _func is None:
            _func = _default_lambda

        return sum([_func(x) for x in self])

    def where(self, _func: Callable = None) -> EnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        return Enumerable(self.type, [x for x in self if _func(x)])
