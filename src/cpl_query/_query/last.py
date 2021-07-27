from typing import Optional

from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument, IndexOutOfRangeException
from cpl_query.extension.iterable_abc import IterableABC


def last_query(_list: IterableABC) -> any:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if len(_list) == 0:
        raise IndexOutOfRangeException()

    return _list[len(_list) - 1]


def last_or_default_query(_list: IterableABC) -> Optional[any]:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if len(_list) == 0:
        return None

    return _list[len(_list) - 1]
