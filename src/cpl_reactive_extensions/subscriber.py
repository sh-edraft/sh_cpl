from typing import Callable

from cpl_core.type import T
from cpl_reactive_extensions.abc.observer import Observer
from cpl_reactive_extensions.subscription import Subscription


class Subscriber(Subscription, Observer):
    def __init__(self, on_next: Callable, on_error: Callable = None, on_complete: Callable = None):
        Subscription.__init__(self)
        self._on_next = on_next
        self._on_error = on_error
        self._on_complete = on_complete

    def next(self, value: T):
        if self._closed:
            raise Exception("Observer is closed")

        self._on_next(value)

    def error(self, ex: Exception):
        if self._on_error is None:
            return
        self._on_error(ex)

    def complete(self):
        self._closed = True
        if self._on_complete is None:
            return

        self._on_complete()
