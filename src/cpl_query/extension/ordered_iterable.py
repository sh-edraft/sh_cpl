from collections import Callable

from iterable import Iterable
from .._query.order_by import then_by_query, then_by_descending_query
from ordered_iterable_abc import OrderedIterableABC


class OrderedIterable(Iterable, OrderedIterableABC):
    r"""Implementation of :class: `cpl_query.extension.Iterable` `cpl_query.extension.OrderedIterableABC`
    """

    def __init__(self):
        Iterable.__init__(self)
        OrderedIterableABC.__init__(self)

    def then_by(self, _func: Callable) -> OrderedIterableABC:
        self._funcs.append(_func)
        return then_by_query(self, lambda *args: [f(*args) for f in self._funcs])

    def then_by_descending(self, _func: Callable) -> OrderedIterableABC:
        self._funcs.append(_func)
        return then_by_descending_query(self, lambda *args: [f(*args) for f in self._funcs])
