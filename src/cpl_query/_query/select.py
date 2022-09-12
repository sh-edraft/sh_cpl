from typing import Callable

from cpl_query.extension.iterable_abc import IterableABC


def select_query(_list: IterableABC, _f: Callable) -> any:
    result = IterableABC()
    result.extend(_f(_o) for _o in _list)
    return result


def select_many_query(_list: IterableABC, _f: Callable) -> any:
    result = IterableABC()
    # The line below is pain. I don't understand anything of it...
    # written on 09.11.2022 by Sven Heidemann
    elements = [_a for _o in _list for _a in _f(_o)]

    result.extend(elements)
    return result
