from collections.abc import Callable

from cpl_query.iterable.iterable import Iterable
from cpl_query.iterable.ordered_iterable_abc import OrderedIterableABC
from cpl_query.query import Query


class OrderedIterable(Iterable, OrderedIterableABC):
    r"""Implementation of :class: `cpl_query.extension.Iterable` `cpl_query.extension.OrderedIterableABC`
    """

    def __init__(self, _t: type = None):
        Iterable.__init__(self, _t)
        OrderedIterableABC.__init__(self, _t)

    def then_by(self, _func: Callable) -> OrderedIterableABC:
        self._funcs.append(_func)
        return Query.then_by(self, lambda *args: [f(*args) for f in self._funcs])

    def then_by_descending(self, _func: Callable) -> OrderedIterableABC:
        self._funcs.append(_func)
        return Query.then_by_descending(self, lambda *args: [f(*args) for f in self._funcs])
