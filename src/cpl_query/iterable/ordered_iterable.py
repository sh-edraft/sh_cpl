from collections.abc import Callable

from cpl_query.exceptions import ArgumentNoneException, ExceptionArgument
from cpl_query.iterable.iterable import Iterable
from cpl_query.iterable.ordered_iterable_abc import OrderedIterableABC


class OrderedIterable(Iterable, OrderedIterableABC):
    r"""Implementation of :class: `cpl_query.extension.Iterable` `cpl_query.extension.OrderedIterableABC`
    """

    def __init__(self, _t: type, _func: Callable = None, _values: Iterable = None):
        Iterable.__init__(self, _t)
        OrderedIterableABC.__init__(self, _t, _func, _values)

    def then_by(self: OrderedIterableABC, _func: Callable) -> OrderedIterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        self._funcs.append(_func)

        return OrderedIterable(self.type, _func, sorted(self, key=lambda *args: [f(*args) for f in self._funcs]))

    def then_by_descending(self: OrderedIterableABC, _func: Callable) -> OrderedIterableABC:
        if self is None:
            raise ArgumentNoneException(ExceptionArgument.list)

        if _func is None:
            raise ArgumentNoneException(ExceptionArgument.func)

        self._funcs.append(_func)
        return OrderedIterable(self.type, _func, sorted(self, key=lambda *args: [f(*args) for f in self._funcs], reverse=True))
