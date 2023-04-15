from typing import Callable, Union, Any, Optional

from cpl_reactive_extensions.abc.operator import Operator
from cpl_reactive_extensions.abc.subscribable import Subscribable
from cpl_reactive_extensions.subscriber import Observer, Subscriber
from cpl_reactive_extensions.subscription import Subscription


class Observable(Subscribable):
    def __init__(self, subscribe: Callable = None):
        Subscribable.__init__(self)
        if subscribe is not None:
            self._subscribe = subscribe

        self._source: Optional[Observable] = None
        self._operator: Optional[Operator] = None

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

    def subscribe(
        self, observer_or_next: Union[Callable, Observer], on_error: Callable = None, on_complete: Callable = None
    ) -> Subscription:
        subscriber = (
            observer_or_next
            if Observable._is_subscriber(observer_or_next)
            else Subscriber(observer_or_next, on_error, on_complete)
        )

        subscriber.add(
            self._operator.call(subscriber, self._source)
            if self._operator is not None
            else self._subscribe(subscriber)
            if self._source is not None
            else self._try_subscribe(subscriber)
        )

        return subscriber

    def _try_subscribe(self, subscriber: Subscriber):
        try:
            return self._subscribe(subscriber)
        except Exception as e:
            subscriber.error(e)

    def _call(self, observer: Observer):
        try:
            self._subscribe(observer)
        except Exception as e:
            observer.error(e)
