from typing import Optional

from cpl_query.extension.iterable_abc import IterableABC


def first_query(_list: IterableABC) -> any:
    if len(_list) == 0:
        raise Exception('Index out of range')

    return _list[0]


def first_or_default_query(_list: IterableABC) -> Optional[any]:
    if len(_list) == 0:
        return None

    return _list[0]
