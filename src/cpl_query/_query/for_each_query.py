from collections import Callable

from cpl_query.extension.iterable_abc import IterableABC


def for_each_query(_list: IterableABC, func: Callable):
    for element in _list:
        func(element)
