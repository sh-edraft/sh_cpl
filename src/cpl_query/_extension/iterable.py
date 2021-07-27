from typing import Optional, Callable

from cpl_query._extension.ordered_iterable import OrderedIterable
from cpl_query.extension.ordered_iterable_abc import OrderedIterableABC
from .._query.all_query import all_query
from .._query.any_query import any_query
from .._query.first_query import first_or_default_query, first_query
from .._query.for_each_query import for_each_query
from .._query.order_by import order_by_query, order_by_descending_query
from .._query.single_query import single_query, single_or_default_query
from .._query.where_query import where_query
from cpl_query.extension.iterable_abc import IterableABC


class Iterable(IterableABC):

    def __init__(self):
        IterableABC.__init__(self)

    def any(self, func: Callable) -> bool:
        return any_query(self, func)

    def all(self, func: Callable) -> bool:
        return all_query(self, func)

    def first(self) -> any:
        return first_query(self)

    def first_or_default(self) -> Optional[any]:
        return first_or_default_query(self)

    def for_each(self, func: Callable):
        for_each_query(self, func)

    def order_by(self, func: Callable) -> OrderedIterableABC:
        res = order_by_query(self, func)
        res.__class__ = OrderedIterable
        return res

    def order_by_descending(self, func: Callable) -> OrderedIterableABC:
        res = order_by_descending_query(self, func)
        res.__class__ = OrderedIterable
        return res

    def single(self) -> any:
        return single_query(self)

    def single_or_default(self) -> Optional[any]:
        return single_or_default_query(self)

    def where(self, func: Callable) -> IterableABC:
        res = where_query(self, func)
        res.__class__ = Iterable
        return res

    def to_list(self) -> list:
        return list(self)
