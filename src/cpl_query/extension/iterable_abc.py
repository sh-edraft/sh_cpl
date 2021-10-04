from abc import ABC, abstractmethod
from typing import Optional, Callable, Union, Iterable


class IterableABC(ABC, list):

    @abstractmethod
    def __init__(self, t: type = None, values: list = None):
        list.__init__(self)

        if t == any:
            t = None
        self._type = t

        if values is not None:
            for value in values:
                self.append(value)

    @property
    def type(self) -> type:
        return self._type

    @abstractmethod
    def any(self, func: Callable) -> bool: pass

    @abstractmethod
    def all(self, func: Callable) -> bool: pass

    def append(self, __object: object) -> None:
        if self._type is not None and type(__object) != self._type and not isinstance(type(__object), self._type):
            raise Exception(f'Unexpected type: {type(__object)}')

        if len(self) == 0 and self._type is None:
            self._type = type(__object)

        super().append(__object)

    @abstractmethod
    def average(self, func: Callable = None) -> Union[int, float, complex]: pass

    @abstractmethod
    def contains(self, value: object) -> bool: pass

    @abstractmethod
    def count(self, func: Callable) -> int: pass

    @abstractmethod
    def distinct(self, func: Callable) -> 'IterableABC': pass

    @abstractmethod
    def element_at(self, index: int) -> any: pass

    @abstractmethod
    def element_at_or_default(self, index: int) -> Optional[any]: pass

    def extend(self, __iterable: Iterable) -> None:
        for value in __iterable:
            self.append(value)

    @abstractmethod
    def last(self) -> any: pass

    @abstractmethod
    def last_or_default(self) -> any: pass

    @abstractmethod
    def first(self) -> any: pass

    @abstractmethod
    def first_or_default(self) -> any: pass

    @abstractmethod
    def for_each(self, func: Callable) -> Union[int, float, complex]: pass

    @abstractmethod
    def max(self, func: Callable = None) -> Union[int, float, complex]: pass

    @abstractmethod
    def min(self, func: Callable = None) -> Union[int, float, complex]: pass

    @abstractmethod
    def order_by(self, func: Callable) -> 'IterableABC': pass

    @abstractmethod
    def order_by_descending(self, func: Callable) -> 'IterableABC': pass

    @abstractmethod
    def reverse(self) -> 'IterableABC': pass

    @abstractmethod
    def single(self) -> any: pass

    @abstractmethod
    def single_or_default(self) -> Optional[any]: pass

    @abstractmethod
    def skip(self, index: int) -> 'IterableABC': pass

    @abstractmethod
    def skip_last(self, index: int) -> 'IterableABC': pass

    @abstractmethod
    def sum(self, func: Callable = None) -> Union[int, float, complex]: pass

    @abstractmethod
    def take(self, index: int) -> 'IterableABC': pass

    @abstractmethod
    def take_last(self, index: int) -> 'IterableABC': pass

    def to_list(self) -> list:
        return list(self)

    @abstractmethod
    def where(self, func: Callable) -> 'IterableABC': pass
