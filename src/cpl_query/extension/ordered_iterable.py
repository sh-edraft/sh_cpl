from abc import ABC
from collections import Callable

from .._query.order_by import then_by_query, then_by_descending_query
from cpl_query.extension.ordered_iterable_abc import OrderedIterableABC


class OrderedIterable(OrderedIterableABC, ABC):

    def __init__(self):
        OrderedIterableABC.__init__(self)

    def then_by(self, _func: Callable) -> OrderedIterableABC:
        self._funcs.append(_func)
        return then_by_query(self, lambda *args: [f(*args) for f in self._funcs])

    def then_by_descending(self, _func: Callable) -> OrderedIterableABC:
        self._funcs.append(_func)
        return then_by_descending_query(self, lambda *args: [f(*args) for f in self._funcs])
