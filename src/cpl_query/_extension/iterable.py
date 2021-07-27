from typing import Optional, Callable, Union

from cpl_query._extension.ordered_iterable import OrderedIterable
from cpl_query.extension.ordered_iterable_abc import OrderedIterableABC
from .._query.all import all_query
from .._query.any import any_query
from .._query.avg import avg_query
from .._query.contains import contains_query
from .._query.count import count_query
from .._query.distinct import distinct_query
from .._query.element_at import element_at_query, element_at_or_default_query
from .._query.first import first_or_default_query, first_query
from .._query.for_each import for_each_query
from .._query.last import last_query, last_or_default_query
from .._query.order_by import order_by_query, order_by_descending_query
from .._query.single import single_query, single_or_default_query
from .._query.where import where_query
from cpl_query.extension.iterable_abc import IterableABC


class Iterable(IterableABC):

    def __init__(self):
        IterableABC.__init__(self)

    def any(self, func: Callable) -> bool:
        return any_query(self, func)

    def all(self, func: Callable) -> bool:
        return all_query(self, func)

    def average(self, t: type, func: Callable) -> Union[int, float, complex]:
        return avg_query(self, t, func)

    def contains(self, value: object) -> bool:
        return contains_query(self, value)

    def count(self, func: Callable = None) -> int:
        return count_query(self, func)

    def distinct(self, func: Callable) -> IterableABC:
        res = distinct_query(self, func)
        res.__class__ = Iterable
        return res

    def element_at(self, index: int) -> any:
        return element_at_query(self, index)

    def element_at_or_default(self, index: int) -> Optional[any]:
        return element_at_or_default_query(self, index)

    def last(self) -> any:
        return last_query(self)

    def last_or_default(self) -> Optional[any]:
        return last_or_default_query(self)

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
