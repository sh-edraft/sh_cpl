from typing import Callable, Union, Optional

from cpl_query._helper import is_number
from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument, InvalidTypeException, IndexOutOfRangeException
from cpl_query.iterable.iterable_abc import IterableABC
from cpl_query.iterable.ordered_iterable_abc import OrderedIterableABC


class Query:

    @staticmethod
    def all(_list: IterableABC, _func: Callable) -> bool:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        result = Query.where(_list, _func)
        return len(result) == len(_list)

    @staticmethod
    def any(_list: IterableABC, _func: Callable) -> bool:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        result = Query.where(_list, _func)
        return len(result) > 0

    @staticmethod
    def avg(_list: IterableABC, _func: Callable) -> Union[int, float, complex]:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None and not is_number(_list.type):
            raise InvalidTypeException()

        average = 0
        count = len(_list)

        for element in _list:
            if _func is not None:
                value = _func(element)

            else:
                value = element

            average += value

        return average / count

    @staticmethod
    def contains(_list: IterableABC, _value: object) -> bool:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _value is None:
            raise ArgumentNoneException(ExceptionArgument.value)

        return _value in _list

    @staticmethod
    def count(_list: IterableABC, _func: Callable = None) -> int:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            return len(_list)

        return len(Query.where(_list, _func))

    @staticmethod
    def distinct(_list: IterableABC, _func: Callable) -> IterableABC:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        result = IterableABC()
        known_values = []
        for element in _list:
            value = _func(element)
            if value in known_values:
                continue

            known_values.append(value)
            result.append(element)

        return result

    @staticmethod
    def element_at(_list: IterableABC, _index: int) -> any:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        return _list[_index]

    @staticmethod
    def element_at_or_default(_list: IterableABC, _index: int) -> any:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        try:
            return _list[_index]
        except IndexError:
            return None

    @staticmethod
    def first(_list: IterableABC) -> any:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(_list) == 0:
            raise IndexOutOfRangeException()

        return _list[0]

    @staticmethod
    def first_or_default(_list: IterableABC) -> Optional[any]:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(_list) == 0:
            return None

        return _list[0]

    @staticmethod
    def last(_list: IterableABC) -> any:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(_list) == 0:
            raise IndexOutOfRangeException()

        return _list[len(_list) - 1]

    @staticmethod
    def last_or_default(_list: IterableABC) -> Optional[any]:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(_list) == 0:
            return None

        return _list[len(_list) - 1]

    @staticmethod
    def for_each(_list: IterableABC, _func: Callable):
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        for element in _list:
            _func(element)

    @staticmethod
    def max(_list: IterableABC, _func: Callable) -> Union[int, float, complex]:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None and not is_number(_list.type):
            raise InvalidTypeException()

        max_value = 0
        for element in _list:
            if _func is not None:
                value = _func(element)
            else:
                value = element

            if value > max_value:
                max_value = value

        return max_value

    @staticmethod
    def min(_list: IterableABC, _func: Callable) -> Union[int, float, complex]:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None and not is_number(_list.type):
            raise InvalidTypeException()

        min_value = 0
        is_first = True
        for element in _list:
            if _func is not None:
                value = _func(element)
            else:
                value = element

            if is_first:
                min_value = value
                is_first = False

            if value < min_value:
                min_value = value

        return min_value

    @staticmethod
    def order_by(_list: IterableABC, _func: Callable) -> OrderedIterableABC:
        result = OrderedIterableABC(_list.type, _func)
        _list.sort(key=_func)
        result.extend(_list)
        return result

    @staticmethod
    def order_by_descending(_list: IterableABC, _func: Callable) -> OrderedIterableABC:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        result = OrderedIterableABC(_list.type, _func)
        _list.sort(key=_func, reverse=True)
        result.extend(_list)
        return result

    @staticmethod
    def then_by(_list: OrderedIterableABC, _func: Callable) -> OrderedIterableABC:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        _list.sort(key=_func)
        return _list

    @staticmethod
    def then_by_descending(_list: OrderedIterableABC, _func: Callable) -> OrderedIterableABC:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        _list.sort(key=_func, reverse=True)
        return _list

    @staticmethod
    def reverse(_list: IterableABC) -> IterableABC:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        result = IterableABC()
        _copied_list = _list.to_list()
        _copied_list.reverse()
        for element in _copied_list:
            result.append(element)

        return result

    @staticmethod
    def select(_list: IterableABC, _f: Callable) -> any:
        result = IterableABC()
        result.extend(_f(_o) for _o in _list)
        return result

    @staticmethod
    def select_many(_list: IterableABC, _f: Callable) -> any:
        result = IterableABC()
        # The line below is pain. I don't understand anything of it...
        # written on 09.11.2022 by Sven Heidemann
        elements = [_a for _o in _list for _a in _f(_o)]

        result.extend(elements)
        return result

    @staticmethod
    def single(_list: IterableABC) -> any:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(_list) > 1:
            raise Exception('Found more than one element')
        elif len(_list) == 0:
            raise Exception('Found no element')

        return _list[0]

    @staticmethod
    def single_or_default(_list: IterableABC) -> Optional[any]:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if len(_list) > 1:
            raise Exception('Index out of range')
        elif len(_list) == 0:
            return None

        return _list[0]

    @staticmethod
    def skip(_list: IterableABC, _index: int) -> IterableABC:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        if _index >= len(_list):
            raise IndexOutOfRangeException()

        result = IterableABC()
        result.extend(_list[_index:])
        return result

    @staticmethod
    def skip_last(_list: IterableABC, _index: int) -> IterableABC:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        index = len(_list) - _index

        if index >= len(_list) or index < 0:
            raise IndexOutOfRangeException()

        result = IterableABC()
        result.extend(_list[:index])
        return result

    @staticmethod
    def take(_list: IterableABC, _index: int) -> IterableABC:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        if _index >= len(_list):
            raise IndexOutOfRangeException()

        result = IterableABC()
        result.extend(_list[:_index])
        return result

    @staticmethod
    def take_last(_list: IterableABC, _index: int) -> IterableABC:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _index is None:
            raise ArgumentNoneException(ExceptionArgument.index)

        index = len(_list) - _index

        if index >= len(_list) or index < 0:
            raise IndexOutOfRangeException()

        result = IterableABC()
        result.extend(_list[index:])
        return result

    @staticmethod
    def sum(_list: IterableABC, _func: Callable) -> Union[int, float, complex]:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None and not is_number(_list.type):
            raise InvalidTypeException()

        result = 0
        for element in _list:
            if _func is not None:
                value = _func(element)
            else:
                value = element

            result += value

        return result

    @staticmethod
    def where(_list: IterableABC, _func: Callable) -> IterableABC:
        if _list is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        result = IterableABC(_list.type)
        for element in _list:
            if _func(element):
                result.append(element)

        return result
