from collections import Callable

from cpl_query._query.where_query import where_query
from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument
from cpl_query.extension.iterable_abc import IterableABC


def count_query(_list: IterableABC, _func: Callable = None) -> int:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None:
        return len(_list)

    return len(where_query(_list, _func))
