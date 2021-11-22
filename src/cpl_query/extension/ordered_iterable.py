from collections import Callable

from cpl_query._query.order_by import then_by_descending_query, then_by_query
from cpl_query.extension.iterable import Iterable
from cpl_query.extension.ordered_iterable_abc import OrderedIterableABC


class OrderedIterable(Iterable, OrderedIterableABC):
    r"""Implementation of :class: `cpl_query.extension.Iterable` `cpl_query.extension.OrderedIterableABC`
    """

    def __init__(self, _t: type = None):
        Iterable.__init__(self, _t)
        OrderedIterableABC.__init__(self, _t)

    def then_by(self, _func: Callable) -> OrderedIterableABC:
        self._funcs.append(_func)
        return then_by_query(self, lambda *args: [f(*args) for f in self._funcs])

    def then_by_descending(self, _func: Callable) -> OrderedIterableABC:
        self._funcs.append(_func)
        return then_by_descending_query(self, lambda *args: [f(*args) for f in self._funcs])
