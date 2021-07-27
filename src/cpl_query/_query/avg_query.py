from typing import Callable, Union

from cpl_query.exceptions import InvalidTypeException, WrongTypeException, ExceptionArgument, ArgumentNoneException
from cpl_query.extension.iterable_abc import IterableABC


def avg_query(_list: IterableABC, _t: type, _func: Callable) -> Union[int, float, complex]:
    average = 0
    count = len(_list)

    if _list is None:
        raise ArgumentNoneException(ExceptionArgument.list)

    if _func is None:
        raise ArgumentNoneException(ExceptionArgument.func)

    if _t != int and _t != float and _t != complex:
        raise InvalidTypeException()

    for element in _list:
        value = _func(element)
        if type(value) != _t:
            raise WrongTypeException()

        average += value

    return average / count

