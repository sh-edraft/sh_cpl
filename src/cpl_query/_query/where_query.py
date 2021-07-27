from collections import Callable

from cpl_query.extension.iterable_abc import IterableABC


def where_query(_list: IterableABC, _func: Callable) -> IterableABC:
    result = IterableABC()
    for element in _list:
        if _func(element):
            result.append(element)

    return result
