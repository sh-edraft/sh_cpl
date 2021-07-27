from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument
from cpl_query.extension.iterable_abc import IterableABC


def contains_query(_list: IterableABC, _value: object) -> bool:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)
    
    if _value is None:
        raise ArgumentNoneException(ExceptionArgument.value)
    
    return _value in _list
