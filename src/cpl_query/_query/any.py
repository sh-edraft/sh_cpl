from collections import Callable

from cpl_query._query.where import where_query
from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument
from cpl_query.extension.iterable_abc import IterableABC


def any_query(_list: IterableABC, _func: Callable) -> bool:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None:
        raise ArgumentNoneException(ExceptionArgument.func)

    result = where_query(_list, _func)
    return len(result) > 0
