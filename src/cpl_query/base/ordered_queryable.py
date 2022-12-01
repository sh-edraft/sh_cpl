from collections.abc import Callable

from cpl_query.base.ordered_queryable_abc import OrderedQueryableABC
from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument
from cpl_query.iterable.iterable import Iterable


class OrderedQueryable(OrderedQueryableABC):
    r"""Implementation of :class: `cpl_query.extension.Iterable` `cpl_query.extension.OrderedIterableABC`
    """

    def __init__(self, _t: type, _values: Iterable = None, _func: Callable = None):
        OrderedQueryableABC.__init__(self, _t, _values, _func)

    def then_by(self: OrderedQueryableABC, _func: Callable) -> OrderedQueryableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        self._funcs.append(_func)

        return OrderedQueryable(self.type, sorted(self, key=lambda *args: [f(*args) for f in self._funcs]), _func)

    def then_by_descending(self: OrderedQueryableABC, _func: Callable) -> OrderedQueryableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        self._funcs.append(_func)
        return OrderedQueryable(self.type, sorted(self, key=lambda *args: [f(*args) for f in self._funcs], reverse=True), _func)
