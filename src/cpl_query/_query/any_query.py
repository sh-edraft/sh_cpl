from collections import Callable

from cpl_query._query.where_query import where_query
from cpl_query.extension.iterable_abc import IterableABC


def any_query(_list: IterableABC, _func: Callable) -> bool:
    result = where_query(_list, _func)
    return len(result) > 0
