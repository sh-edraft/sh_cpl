from typing import Callable, Union

from cpl_reactive_extensions.observer import Observer


class Observable:
    def __init__(self, callback: Callable = None):
        self._callback = callback

        self._observers: list[Observer] = []

    @staticmethod
    def from_list(values: list):
        i = 0

        def callback(x: Observer):
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
    ) -> Observer:
        if isinstance(observer_or_next, Callable):
            observer = Observer(observer_or_next, on_error, on_complete)
        elif isinstance(observer_or_next, Observable):
            observer = observer_or_next
        else:
            observer = observer_or_next

        if self._callback is None:
            self._observers.append(observer)
            return observer

        if len(observer._observers) > 0:
            for observer in observer._observers:
                self._call(observer)
        else:
            self._call(observer)

        return observer

    def _call(self, observer: Observer):
        try:
            self._callback(observer)
        except Exception as e:
            observer.error(e)
