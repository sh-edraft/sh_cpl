from typing import Optional, Callable

from .._query.any_query import any_query
from .._query.first_query import first_or_default_query, first_query
from .._query.for_each_query import for_each_query
from .._query.single_query import single_query, single_or_default_query
from .._query.where_query import where_query
from cpl_query.extension.iterable_abc import IterableABC


class List(IterableABC):

    def __init__(self):
        IterableABC.__init__(self)

    def any(self, func: str) -> bool:
        return any_query(self, func)

    def first(self) -> any:
        return first_query(self)

    def first_or_default(self) -> Optional[any]:
        return first_or_default_query(self)

    def for_each(self, func: Callable):
        for_each_query(self, func)

    def single(self) -> any:
        return single_query(self)

    def single_or_default(self) -> Optional[any]:
        return single_or_default_query(self)

    def where(self, func: str) -> IterableABC:
        res = where_query(self, func)
        res.__class__ = List
        return res

    def to_list(self) -> list:
        return list(self)
