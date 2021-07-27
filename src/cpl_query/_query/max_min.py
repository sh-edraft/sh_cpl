from collections import Callable
from typing import Union

from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument, InvalidTypeException
from cpl_query.extension.iterable_abc import IterableABC


def max_query(_list: IterableABC, _t: type, _func: Callable) -> Union[int, float, complex]:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None:
        raise ArgumentNoneException(ExceptionArgument.func)

    if _t != int and _t != float and _t != complex:
        raise InvalidTypeException()

    max_value = _t()
    for element in _list:
        value = _func(element)
        if value > max_value:
            max_value = value

    return max_value


def min_query(_list: IterableABC, _t: type, _func: Callable) -> Union[int, float, complex]:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None:
        raise ArgumentNoneException(ExceptionArgument.func)

    if _t != int and _t != float and _t != complex:
        raise InvalidTypeException()

    min_value = _t()
    is_first = True
    for element in _list:
        value = _func(element)
        if is_first:
            min_value = value
            is_first = False

        if value < min_value:
            min_value = value

    return min_value
