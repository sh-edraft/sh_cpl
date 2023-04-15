from typing import Callable, Union, Optional

from cpl_reactive_extensions.abc.subscribable import Subscribable
from cpl_reactive_extensions.subscriber import Observer, Subscriber
from cpl_reactive_extensions.subscription import Subscription


class Observable(Subscribable):
    def __init__(self, callback: Callable = None):
        Subscribable.__init__(self)
        self._callback = callback

        self._subscribers: list[Observer] = []

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

    def subscribe(
        self, observer_or_next: Union[Callable, Observer], on_error: Callable = None, on_complete: Callable = None
    ) -> Subscription:
        observable: Optional[Observable] = None
        if isinstance(observer_or_next, Observable):
            observable = observer_or_next

        if isinstance(observer_or_next, Callable):
            subscriber = Subscriber(observer_or_next, on_error, on_complete)
        else:
            subscriber = observer_or_next

        if self._callback is None:
            self._subscribers.append(subscriber)
            return subscriber

        if observable is not None and len(observable._subscribers) > 0:
            for subscriber in observable._subscribers:
                self._call(subscriber)
        else:
            self._call(subscriber)

        return subscriber

    def _call(self, observer: Observer):
        try:
            self._callback(observer)
        except Exception as e:
            observer.error(e)
