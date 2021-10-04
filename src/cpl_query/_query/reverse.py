from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument
from cpl_query.extension.iterable_abc import IterableABC


def reverse_query(_list: IterableABC) -> IterableABC:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    result = IterableABC()
    _copied_list = _list.to_list()
    _copied_list.reverse()
    for element in _copied_list:
        result.append(element)

    return result
