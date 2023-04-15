from typing import Callable

from cpl_reactive_extensions.observer import Observer


class Observable:
    def __init__(self, callback: Callable):
        self._callback = callback
        self._subscriptions: list[Callable] = []

    def _run_subscriptions(self):
        for callback in self._subscriptions:
            callback()

    def subscribe(self, observer: Observer):
        try:
            self._callback(observer)
        except Exception as e:
            observer.error(e)
