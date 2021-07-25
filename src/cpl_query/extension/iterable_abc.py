from abc import ABC, abstractmethod
from typing import Optional, Callable


class IterableABC(ABC, list):

    @abstractmethod
    def __init__(self):
        list.__init__(self)

    @abstractmethod
    def any(self, func: str) -> bool: pass

    @abstractmethod
    def first(self) -> any: pass

    @abstractmethod
    def first_or_default(self) -> any: pass

    @abstractmethod
    def for_each(self, func: Callable): pass

    @abstractmethod
    def single(self): pass

    @abstractmethod
    def single_or_default(self) -> Optional[any]: pass

    @abstractmethod
    def where(self, func: str) -> 'IterableABC': pass
