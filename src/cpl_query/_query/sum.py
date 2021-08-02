from collections import Callable
from typing import Union

from cpl_query._helper import is_number
from cpl_query.exceptions import ExceptionArgument, ArgumentNoneException, InvalidTypeException
from cpl_query.extension.iterable_abc import IterableABC


def sum_query(_list: IterableABC, _func: Callable) -> Union[int, float, complex]:
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
