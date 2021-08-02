from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument
from cpl_query.extension.iterable_abc import IterableABC


def element_at_query(_list: IterableABC, _index: int) -> any:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _index is None:
        raise ArgumentNoneException(ExceptionArgument.index)

    return _list[_index]


def element_at_or_default_query(_list: IterableABC, _index: int) -> any:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _index is None:
        raise ArgumentNoneException(ExceptionArgument.index)

    try:
        return _list[_index]
    except IndexError:
        return None
