from typing import Callable, Union

from cpl_query._helper import is_number
from cpl_query.exceptions import InvalidTypeException, WrongTypeException, ExceptionArgument, ArgumentNoneException
from cpl_query.extension.iterable_abc import IterableABC


def avg_query(_list: IterableABC, _func: Callable) -> Union[int, float, complex]:
    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None and not is_number(_list.type):
        raise InvalidTypeException()

    average = 0
    count = len(_list)

    for element in _list:
        if _func is not None:
            value = _func(element)

        else:
            value = element

        average += value

    return average / count
