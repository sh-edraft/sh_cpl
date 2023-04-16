from typing import Callable

from cpl_core.type import T
from cpl_reactive_extensions.abc.observer import Observer
from cpl_reactive_extensions.subscription import Subscription
from cpl_reactive_extensions.type import ObserverOrCallable


class Subscriber(Subscription, Observer):
    def __init__(
        self, on_next_or_observer: ObserverOrCallable, on_error: Callable = None, on_complete: Callable = None
    ):
        self.is_stopped = False
        Subscription.__init__(self)
        if isinstance(on_next_or_observer, Observer):
            self._on_next = on_next_or_observer.next
            self._on_error = on_next_or_observer.error
            self._on_complete = on_next_or_observer.complete
        else:
            self._on_next = on_next_or_observer
            self._on_error = on_error
            self._on_complete = on_complete

    def _next(self, value: T):
        self._on_next(value)

    def next(self, value: T):
        if self.is_stopped:
            raise Exception("Observer is closed")

        self._next(value)

    def _error(self, ex: Exception):
        try:
            self._on_error(ex)
        finally:
            self.unsubscribe()

    def error(self, ex: Exception):
        if self.is_stopped:
            return
        self._error(ex)

    def _complete(self):
        try:
            self._on_complete()
        finally:
            self.unsubscribe()

    def complete(self):
        if self.is_stopped:
            return

        self.is_stopped = True
        self._complete()

    def unsubscribe(self):
        if self._closed:
            return

        self.is_stopped = True
        Subscription.unsubscribe(self)
        self._on_next = None
        self._on_error = None
        self._on_complete = None
