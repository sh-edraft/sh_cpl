from cpl_query.extension.iterable_abc import IterableABC


def where_query(_list: IterableABC, _func: str) -> IterableABC:
    result = IterableABC()
    for element in _list:
        element_type = type(element).__name__
        if element_type in _func:
            func = _func.replace(element_type, 'element')
            if eval(func):
                result.append(element)

    return result
