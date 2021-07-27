from collections import Callable

from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument
from cpl_query.extension.iterable_abc import IterableABC


def distinct_query(_list: IterableABC, _func: Callable) -> IterableABC:
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
