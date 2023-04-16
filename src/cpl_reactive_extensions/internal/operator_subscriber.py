from typing import Callable

from cpl_core.type import T
from cpl_reactive_extensions.abc.observer import Observer
from cpl_reactive_extensions.internal.subscriber import Subscriber


class OperatorSubscriber(Subscriber, Observer):
    def __init__(
        self,
        destination: Subscriber,
        on_next: Callable = None,
        on_error: Callable = None,
        on_complete: Callable = None,
        on_finalize: Callable = None,
        should_unsubscribe: Callable = None,
    ):
        Subscriber.__init__(self, destination)
        self._on_finalize = on_finalize
        self._should_unsubscribe = should_unsubscribe

        def on_next_wrapper(value: T):
            try:
                on_next(value)
            except Exception as e:
                destination.error(e)

        self._on_next = on_next_wrapper if on_next is not None else self._on_next

        def on_error_wrapper(value: T):
            try:
                on_error(value)
            except Exception as e:
                destination.error(e)
            finally:
                self.unsubscribe()

        self._on_error = on_error_wrapper if on_error is not None else self._on_error

        def on_complete_wrapper(value: T):
            try:
                on_complete(value)
            except Exception as e:
                destination.error(e)
            finally:
                self.unsubscribe()

        self._on_complete = on_complete_wrapper if on_complete is not None else self._on_complete

    def unsubscribe(self):
        if self._should_unsubscribe is not None and not self._should_unsubscribe():
            return
        Subscriber.unsubscribe(self)
        if not self.closed and self._on_finalize is not None:
            self._on_finalize()
