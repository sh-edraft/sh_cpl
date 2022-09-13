from typing import Callable, Optional, Union

from cpl_query.iterable.iterable_abc import IterableABC
from cpl_query.iterable.ordered_iterable_abc import OrderedIterableABC
from cpl_query.query import Query


class Iterable(IterableABC):

    def __init__(self, t: type = None, values: list = None):
        IterableABC.__init__(self, t, values)

    def any(self, func: Callable) -> bool:
        return Query.any(self, func)

    def all(self, func: Callable) -> bool:
        return Query.all(self, func)

    def average(self, func: Callable = None) -> Union[int, float, complex]:
        return Query.avg(self, func)

    def contains(self, value: object) -> bool:
        return Query.contains(self, value)

    def count(self, func: Callable = None) -> int:
        return Query.count(self, func)

    def distinct(self, func: Callable = None) -> IterableABC:
        return self.__to_self(Query.distinct(self, func))

    def element_at(self, index: int) -> any:
        return Query.element_at(self, index)

    def element_at_or_default(self, index: int) -> Optional[any]:
        return Query.element_at_or_default(self, index)

    def last(self) -> any:
        return Query.last(self)

    def last_or_default(self) -> Optional[any]:
        return Query.last_or_default(self)

    def first(self) -> any:
        return Query.first(self)

    def first_or_default(self) -> Optional[any]:
        return Query.first_or_default(self)

    def for_each(self, func: Callable):
        Query.for_each(self, func)

    def max(self, func: Callable = None) -> Union[int, float, complex]:
        return Query.max(self, func)

    def min(self, func: Callable = None) -> Union[int, float, complex]:
        return Query.min(self, func)

    def order_by(self, func: Callable) -> OrderedIterableABC:
        res = Query.order_by(self, func)
        from cpl_query.iterable.ordered_iterable import OrderedIterable
        res.__class__ = OrderedIterable
        return res

    def order_by_descending(self, func: Callable) -> OrderedIterableABC:
        res = Query.order_by_descending(self, func)
        from cpl_query.iterable.ordered_iterable import OrderedIterable
        res.__class__ = OrderedIterable
        return res

    def reverse(self) -> IterableABC:
        return Query.reverse(self)

    def single(self) -> any:
        return Query.single(self)

    def single_or_default(self) -> Optional[any]:
        return Query.single_or_default(self)

    def select(self, _f: Callable) -> IterableABC:
        return self.__to_self(Query.select(self, _f))

    def select_many(self, _f: Callable) -> IterableABC:
        return self.__to_self(Query.select_many(self, _f))

    def skip(self, index: int) -> IterableABC:
        return self.__to_self(Query.skip(self, index))

    def skip_last(self, index: int) -> IterableABC:
        return self.__to_self(Query.skip_last(self, index))

    def sum(self, func: Callable = None) -> Union[int, float, complex]:
        return Query.sum(self, func)

    def take(self, index: int) -> IterableABC:
        return self.__to_self(Query.take(self, index))

    def take_last(self, index: int) -> IterableABC:
        return self.__to_self(Query.take_last(self, index))

    def where(self, func: Callable) -> IterableABC:
        return self.__to_self(Query.where(self, func))

    @staticmethod
    def __to_self(obj: IterableABC) -> IterableABC:
        obj.__class__ = Iterable
        return obj
