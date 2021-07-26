from collections import Callable

from cpl_query.extension.iterable_abc import IterableABC


def where_query(_list: IterableABC, _func: Callable) -> IterableABC:
    result = IterableABC()
    for element in _list:
        element_type = type(element).__name__
        if _func(element):
            result.append(element)
        # if element_type in _func:
            # func = _func.replace(element_type, 'element')
            # if eval(func):
            #     result.append(element)

    return result
