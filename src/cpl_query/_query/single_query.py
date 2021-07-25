from typing import Optional

from cpl_query.extension.iterable_abc import IterableABC


def single_query(_list: IterableABC) -> any:
    if len(_list) > 1:
        raise Exception('Found more than one element')
    elif len(_list) == 0:
        raise Exception('Found no element')

    return _list[0]


def single_or_default_query(_list: IterableABC) -> Optional[any]:
    if len(_list) > 1:
        raise Exception('Index out of range')
    elif len(_list) == 0:
        return None

    return _list[0]
