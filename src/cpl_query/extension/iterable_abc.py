from abc import ABC, abstractmethod
from typing import Optional, Callable


class IterableABC(ABC, list):

    @abstractmethod
    def __init__(self):
        list.__init__(self)

    @abstractmethod
    def any(self, func: Callable) -> bool: pass

    @abstractmethod
    def all(self, func: Callable) -> bool: pass

    @abstractmethod
    def first(self) -> any: pass

    @abstractmethod
    def first_or_default(self) -> any: pass

    @abstractmethod
    def for_each(self, func: Callable): pass

    @abstractmethod
    def order_by(self, func: Callable): pass

    @abstractmethod
    def order_by_descending(self, func: Callable): pass

    @abstractmethod
    def single(self): pass

    @abstractmethod
    def single_or_default(self) -> Optional[any]: pass

    @abstractmethod
    def where(self, func: Callable) -> 'IterableABC': pass
