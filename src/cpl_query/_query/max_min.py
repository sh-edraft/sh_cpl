from collections import Callable
from typing import Union

from cpl_query._helper import is_number
from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument, InvalidTypeException, WrongTypeException
from cpl_query.extension.iterable_abc import IterableABC


def max_query(_list: IterableABC, _func: Callable) -> Union[int, float, complex]:
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


def min_query(_list: IterableABC, _func: Callable) -> Union[int, float, complex]:
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
