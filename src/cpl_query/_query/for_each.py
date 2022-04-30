from collections.abc import Callable

from cpl_query.exceptions import ExceptionArgument, ArgumentNoneException
from cpl_query.extension.iterable_abc import IterableABC


def for_each_query(_list: IterableABC, _func: Callable):
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None:
        raise ArgumentNoneException(ExceptionArgument.func)

    for element in _list:
        _func(element)
