from cpl_query.extension.iterable_abc import IterableABC


def contains_query(_list: IterableABC, value: object) -> bool:
    return value in _list
