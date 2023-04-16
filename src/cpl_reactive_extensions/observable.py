from __future__ import annotations

from typing import Callable, Any, Optional

from cpl_core.type import T
from cpl_reactive_extensions.abc.observer import Observer
from cpl_reactive_extensions.abc.subscribable import Subscribable
from cpl_reactive_extensions.internal.subscriber import Subscriber
from cpl_reactive_extensions.internal.subscription import Subscription
from cpl_reactive_extensions.type import ObserverOrCallable


class Observable(Subscribable):
    def __init__(self, subscribe: Callable = None):
        Subscribable.__init__(self)
        if subscribe is not None:
            self._subscribe = subscribe

        self._source: Optional[Observable] = None
        self._operator: Optional[Callable] = None

    @staticmethod
    def from_observable(obs: Observable):
        def inner(subscriber: Subscriber):
            if "subscribe" not in dir(obs):
                raise TypeError("Unable to lift unknown Observable type")

            return obs.subscribe(subscriber)

        return Observable(inner)

    @staticmethod
    def from_list(values: list):
        i = 0

        def callback(x: Subscriber):
            nonlocal i
            if i == len(values):
                i = 0
                x.complete()
            else:
                x.next(values[i])
                i += 1

                if not x.closed:
                    callback(x)

        observable = Observable(callback)
        return observable

    def lift(self, operator: Callable) -> Observable:
        observable = Observable()
        observable._source = self
        observable._operator = operator
        return observable

    @staticmethod
    def _is_observer(value: Any) -> bool:
        return isinstance(value, Observer)

    @staticmethod
    def _is_subscription(value: Any) -> bool:
        return isinstance(value, Subscription)

    @staticmethod
    def _is_subscriber(value: Any) -> bool:
        return isinstance(value, Subscriber) or Observable._is_observer(value) and Observable._is_subscription(value)

    def _subscribe(self, subscriber: Subscriber) -> Subscription:
        return self._source.subscribe(subscriber)

    def _try_subscribe(self, subscriber: Subscriber) -> Subscription:
        try:
            return self._subscribe(subscriber)
        except Exception as e:
            subscriber.error(e)

    def subscribe(
        self, observer_or_next: ObserverOrCallable, on_error: Callable = None, on_complete: Callable = None
    ) -> Subscription:
        subscriber = (
            observer_or_next
            if Observable._is_subscriber(observer_or_next)
            else Subscriber(observer_or_next, on_error, on_complete)
        )

        subscriber.add(
            self._operator(subscriber, self._source)
            if self._operator is not None
            else self._subscribe(subscriber)
            if self._source is not None
            else self._try_subscribe(subscriber)
        )

        return subscriber

    def pipe(self, *args) -> Observable:
        return self._pipe_from_array(args)(self)

    def _pipe_from_array(self, args):
        if len(args) == 0:
            return lambda x: x

        if len(args) == 1:
            return args[0]

        def piped(input: T):
            return Observable._reduce(lambda prev, fn: fn(prev), input)

        return piped

    @staticmethod
    def _reduce(func: Callable, input: T):
        return func(input)
