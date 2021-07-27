from typing import Optional

from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument
from cpl_query.extension.iterable_abc import IterableABC


def first_query(_list: IterableABC) -> any:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if len(_list) == 0:
        raise Exception('Index out of range')

    return _list[0]


def first_or_default_query(_list: IterableABC) -> Optional[any]:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if len(_list) == 0:
        return None

    return _list[0]
