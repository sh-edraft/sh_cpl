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
        if _func is None:
            _func = _default_lambda

        return self.where(_func).count() == self.count()

    def any(self, _func: Callable = None) -> bool:
        if _func is None:
            _func = _default_lambda

        return self.where(_func).count() > 0

    def average(self, _func: Callable = None) -> Union[int, float, complex]:
        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        return self.sum(_func) / self.count()

    def contains(self, _value: object) -> bool:
        if _value is None:
            raise ArgumentNoneException(ExceptionArgument.value)

        return self.where(lambda x: x == _value).count() > 0

    def count(self, _func: Callable = None) -> int:
        if _func is None:
            return self.__len__()

        return self.where(_func).__len__()

    def distinct(self, _func: Callable = None) -> 'Iterable':
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
        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        return self[_index]

    def element_at_or_default(self, _index: int) -> any:
        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        try:
            return self[_index]
        except IndexError:
            return None

    def first(self) -> any:
        if len(self) == 0:
            raise IndexOutOfRangeException()

        return self[0]

    def first_or_default(self) -> Optional[any]:
        if len(self) == 0:
            return None

        return self[0]

    def group_by(self, _func: Callable = None) -> 'Iterable':
        if _func is None:
            _func = _default_lambda
        groups = {}

        for v in self:
            value = _func(v)
            if v not in groups:
                groups[value] = Iterable(type(v))

            groups[value].append(v)

        return Iterable(Iterable).extend(groups.values())

    def last(self) -> any:
        if len(self) == 0:
            raise IndexOutOfRangeException()

        return self[len(self) - 1]

    def last_or_default(self) -> Optional[any]:
        if len(self) == 0:
            return None

        return self[len(self) - 1]

    def for_each(self, _func: Callable = None) -> 'Iterable':
        if _func is not None:
            for element in self:
                _func(element)

        return self

    def max(self, _func: Callable = None) -> Union[int, float, complex]:
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
        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        if _func is None:
            _func = _default_lambda

        return _func(min(self, key=_func))

    def order_by(self, _func: Callable = None) -> OrderedIterableABC:
        if _func is None:
            _func = _default_lambda

        from cpl_query.iterable.ordered_iterable import OrderedIterable
        return OrderedIterable(self.type, _func, sorted(self, key=_func))

    def order_by_descending(self, _func: Callable = None) -> OrderedIterableABC:
        if _func is None:
            _func = _default_lambda

        from cpl_query.iterable.ordered_iterable import OrderedIterable
        return OrderedIterable(self.type, _func, sorted(self, key=_func, reverse=True))

    def reverse(self) -> 'Iterable':
        return Iterable().extend(reversed(self))

    def select(self, _func: Callable = None) -> 'Iterable':
        if _func is None:
            _func = _default_lambda

        result = Iterable()
        result.extend(_func(_o) for _o in self)
        return result

    def select_many(self, _func: Callable = None) -> 'Iterable':
        result = Iterable()
        # The line below is pain. I don't understand anything of it...
        # written on 09.11.2022 by Sven Heidemann
        elements = [_a for _o in self for _a in _func(_o)]

        result.extend(elements)
        return result

    def single(self) -> any:
        if len(self) > 1:
            raise Exception('Found more than one element')
        elif len(self) == 0:
            raise Exception('Found no element')

        return self[0]

    def single_or_default(self) -> Optional[any]:
        if len(self) > 1:
            raise Exception('Index out of range')
        elif len(self) == 0:
            return None

        return self[0]

    def skip(self, _index: int) -> 'Iterable':
        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        return Iterable(self.type, values=self[_index:])

    def skip_last(self, _index: int) -> 'Iterable':
        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        index = len(self) - _index

        result = Iterable()
        result.extend(self[:index])
        return result

    def sum(self, _func: Callable = None) -> Union[int, float, complex]:
        if _func is None and not is_number(self.type):
            raise InvalidTypeException()

        if _func is None:
            _func = _default_lambda

        result = 0
        for x in self:
            result += _func(x)

        return result

    def take(self, _index: int) -> 'Iterable':
        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        result = Iterable()
        result.extend(self[:_index])
        return result

    def take_last(self, _index: int) -> 'Iterable':
        index = len(self) - _index

        if index >= len(self) or index < 0:
            raise IndexOutOfRangeException()

        result = Iterable()
        result.extend(self[index:])
        return result

    def where(self, _func: Callable = None) -> 'Iterable':
        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        if _func is None:
            _func = _default_lambda

        result = Iterable(self.type)
        for element in self:
            if _func(element):
                result.append(element)

        return result
