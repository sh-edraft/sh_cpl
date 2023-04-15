from typing import Any, Optional

from cpl_core.type import T
from cpl_reactive_extensions.abc.observer import Observer
from cpl_reactive_extensions.observable import Observable
from cpl_reactive_extensions.subscriber import Subscriber
from cpl_reactive_extensions.subscription import Subscription


class Subject(Observable, Observer):
    def __init__(self, _t: type):
        Observable.__init__(self)

        self.is_closed = False
        self._t = _t
        self._current_observers: Optional[list[Observer]] = None

        self.closed = False
        self.observers: list[Observer] = []
        self.is_stopped = False
        self.has_error = False
        self.raised_error: Any = None

    @property
    def observed(self) -> bool:
        return len(self.observers) > 0

    def _raise_if_closed(self):
        if not self.closed:
            return
        raise Exception("Subject is unsubscribed!")

    def next(self, value: T):
        self._raise_if_closed()

        if not isinstance(value, self._t):
            raise TypeError()

        if self.is_stopped:
            return

        if self._current_observers is None:
            self._current_observers = self.observers

        for observer in self._current_observers:
            observer.next(value)

    def error(self, error: Exception):
        self._raise_if_closed()
        if self.is_stopped:
            return

        self.is_stopped = True
        self.has_error = self.is_stopped
        for observer in self.observers:
            observer.error(error)

    def complete(self):
        self._raise_if_closed()

        if self.is_stopped:
            return

        self.is_stopped = True
        for observer in self.observers:
            observer.complete()

    def unsubscribe(self):
        self.is_stopped = True
        self.is_closed = True
        self._current_observers = None
        self.observers = []

    def _try_subscribe(self, subscriber: Subscriber):
        self._raise_if_closed()
        return super()._try_subscribe(subscriber)

    def _subscribe(self, subscriber: Subscriber) -> Subscription:
        self._raise_if_closed()
        self._check_finalized_statuses(subscriber)
        return self._inner_subscribe(subscriber)

    def _check_finalized_statuses(self, subscriber: Subscriber):
        if self.has_error:
            subscriber.error(self.raised_error)
        elif self.is_stopped:
            subscriber.complete()

    def _inner_subscribe(self, subscriber: Subscriber) -> Optional[Subscription]:
        if self.has_error or self.is_stopped:
            return Subscription.empty()

        self._current_observers = None
        self.observers.append(subscriber)

        def _initial():
            self._current_observers = None
            self.observers.remove(subscriber)

        return Subscription(_initial)
