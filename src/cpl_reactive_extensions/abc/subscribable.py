from abc import ABC, abstractmethod
from typing import Union, Callable

from cpl_reactive_extensions.abc.observer import Observer
from cpl_reactive_extensions.abc.unsubscribable import Unsubscribable


class Subscribable(ABC):
    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def subscribe(
        self, observer_or_next: Union[Callable, Observer], on_error: Callable = None, on_complete: Callable = None
    ) -> Unsubscribable:
        pass
