from collections import Callable

from cpl_query.exceptions import ExceptionArgument, ArgumentNoneException
from cpl_query.extension.iterable_abc import IterableABC
from cpl_query.extension.ordered_iterable_abc import OrderedIterableABC


def order_by_query(_list: IterableABC, _func: Callable) -> OrderedIterableABC:
    result = OrderedIterableABC(_func)
    _list.sort(key=_func)
    result.extend(_list)
    return result


def order_by_descending_query(_list: IterableABC, _func: Callable) -> OrderedIterableABC:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None:
        raise ArgumentNoneException(ExceptionArgument.func)

    result = OrderedIterableABC(_func)
    _list.sort(key=_func, reverse=True)
    result.extend(_list)
    return result


def then_by_query(_list: OrderedIterableABC, _func: Callable) -> OrderedIterableABC:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None:
        raise ArgumentNoneException(ExceptionArgument.func)

    _list.sort(key=_func)
    return _list


def then_by_descending_query(_list: OrderedIterableABC, _func: Callable) -> OrderedIterableABC:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None:
        raise ArgumentNoneException(ExceptionArgument.func)

    _list.sort(key=_func, reverse=True)
    return _list
