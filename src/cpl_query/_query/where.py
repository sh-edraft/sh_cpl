from collections import Callable

from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument
from cpl_query.extension.iterable_abc import IterableABC


def where_query(_list: IterableABC, _func: Callable) -> IterableABC:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None:
        raise ArgumentNoneException(ExceptionArgument.func)

    result = IterableABC(_list.type)
    for element in _list:
        if _func(element):
            result.append(element)

    return result
