from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument, IndexOutOfRangeException
from cpl_query.extension.iterable_abc import IterableABC


def skip_query(_list: IterableABC, _index: int) -> IterableABC:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _index is None:
        raise ArgumentNoneException(ExceptionArgument.index)

    if _index >= len(_list):
        raise IndexOutOfRangeException()

    result = IterableABC()
    result.extend(_list[_index:])
    return result


def skip_last_query(_list: IterableABC, _index: int) -> IterableABC:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _index is None:
        raise ArgumentNoneException(ExceptionArgument.index)

    index = len(_list) - _index

    if index >= len(_list) or index < 0:
        raise IndexOutOfRangeException()

    result = IterableABC()
    result.extend(_list[:index])
    return result


def take_query(_list: IterableABC, _index: int) -> IterableABC:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _index is None:
        raise ArgumentNoneException(ExceptionArgument.index)

    if _index >= len(_list):
        raise IndexOutOfRangeException()

    result = IterableABC()
    result.extend(_list[:_index])
    return result


def take_last_query(_list: IterableABC, _index: int) -> IterableABC:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _index is None:
        raise ArgumentNoneException(ExceptionArgument.index)

    index = len(_list) - _index

    if index >= len(_list) or index < 0:
        raise IndexOutOfRangeException()

    result = IterableABC()
    result.extend(_list[index:])
    return result
