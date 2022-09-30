from collections.abc import Callable
from typing import Iterable

from cpl_query.enumerable.enumerable import Enumerable
from cpl_query.enumerable.ordered_enumerable_abc import OrderedEnumerableABC
from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument


class OrderedEnumerable(Enumerable, OrderedEnumerableABC):
    r"""Implementation of :class: `cpl_query.extension.Enumerable` `cpl_query.extension.OrderedEnumerableABC`
    """

    def __init__(self, _t: type, _func: Callable = None, _values: Iterable = None):
        Enumerable.__init__(self, _t)
        OrderedEnumerableABC.__init__(self, _t, _func, _values)

    def then_by(self: OrderedEnumerableABC, _func: Callable) -> OrderedEnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        self._funcs.append(_func)

        return OrderedEnumerable(self.type, _func, sorted(self, key=lambda *args: [f(*args) for f in self._funcs]))

    def then_by_descending(self: OrderedEnumerableABC, _func: Callable) -> OrderedEnumerableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        self._funcs.append(_func)
        return OrderedEnumerable(self.type, _func, sorted(self, key=lambda *args: [f(*args) for f in self._funcs], reverse=True))
