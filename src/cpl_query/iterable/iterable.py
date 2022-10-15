from typing import Callable, Optional, Union, Iterable as IterableType

from cpl_query._helper import is_number
from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument, InvalidTypeException, IndexOutOfRangeException
from cpl_query.iterable.iterable_abc import IterableABC
from cpl_query.iterable.ordered_iterable_abc import OrderedIterableABC


def _default_lambda(x: object):
    return x


class Iterable(IterableABC):

    def __init__(self, t: type = None, values: IterableType = None):
        IterableABC.__init__(self, t, values)

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

    def distinct(self, _func: Callable = None) -> IterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            _func = _default_lambda

        result = Iterable()
        known_values = []
        for element in self:
            value = _func(element)
            if value in known_values:
                continue

            known_values.append(value)
            result.append(element)

        return result

    def element_at(self, _index: int) -> any:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        return self[_index]

    def element_at_or_default(self, _index: int) -> any:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        try:
            return self[_index]
        except IndexError:
            return None

    def first(self: IterableABC) -> any:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(self) == 0:
            raise IndexOutOfRangeException()

        return self[0]

    def first_or_default(self: IterableABC) -> Optional[any]:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(self) == 0:
            return None

        return self[0]

    def last(self: IterableABC) -> any:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(self) == 0:
            raise IndexOutOfRangeException()

        return self[len(self) - 1]

    def last_or_default(self: IterableABC) -> Optional[any]:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(self) == 0:
            return None

        return self[len(self) - 1]

    def for_each(self, _func: Callable = None):
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            _func = _default_lambda

        for element in self:
            _func(element)

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

    def order_by(self, _func: Callable = None) -> OrderedIterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            _func = _default_lambda

        from cpl_query.iterable.ordered_iterable import OrderedIterable
        return OrderedIterable(self.type, _func, sorted(self, key=_func))

    def order_by_descending(self, _func: Callable = None) -> OrderedIterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            _func = _default_lambda

        from cpl_query.iterable.ordered_iterable import OrderedIterable
        return OrderedIterable(self.type, _func, sorted(self, key=_func, reverse=True))

    def reverse(self: IterableABC) -> IterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        return Iterable().extend(reversed(self.to_list()))

    def select(self, _func: Callable = None) -> IterableABC:
        if _func is None:
            _func = _default_lambda

        result = Iterable()
        result.extend(_func(_o) for _o in self)
        return result

    def select_many(self, _func: Callable = None) -> IterableABC:
        if _func is None:
            _func = _default_lambda

        result = Iterable()
        # The line below is pain. I don't understand anything of it...
        # written on 09.11.2022 by Sven Heidemann
        elements = [_a for _o in self for _a in _func(_o)]

        result.extend(elements)
        return result

    def single(self: IterableABC) -> any:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(self) > 1:
            raise Exception('Found more than one element')
        elif len(self) == 0:
            raise Exception('Found no element')

        return self[0]

    def single_or_default(self: IterableABC) -> Optional[any]:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(self) > 1:
            raise Exception('Index out of range')
        elif len(self) == 0:
            return None

        return self[0]

    def skip(self, _index: int) -> IterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        return Iterable(self.type, values=self[_index:])

    def skip_last(self, _index: int) -> IterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        index = len(self) - _index

        result = Iterable()
        result.extend(self[:index])
        return result

    def take(self, _index: int) -> IterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        result = Iterable()
        result.extend(self[:_index])
        return result

    def take_last(self, _index: int) -> IterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        index = len(self) - _index

        if index >= len(self) or index < 0:
            raise IndexOutOfRangeException()

        result = Iterable()
        result.extend(self[index:])
        return result

    def sum(self, _func: Callable = None) -> Union[int, float, complex]:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        if _func is None:
            _func = _default_lambda

        return sum([_func(x) for x in self])

    def where(self, _func: Callable = None) -> IterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        if _func is None:
            _func = _default_lambda

        result = Iterable(self.type)
        for element in self:
            if _func(element):
                result.append(element)

        return result