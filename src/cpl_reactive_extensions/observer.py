from typing import Callable

from cpl_core.type import T


class Observer:
    def __init__(self, on_next: Callable, on_error: Callable = None, on_complete: Callable = None):
        self._on_next = on_next
        self._on_error = on_error if on_error is not None else lambda err: err
        self._on_complete = on_complete if on_complete is not None else lambda x: x

    def next(self, value: T):
        self._on_next(value)

    def error(self, ex: Exception):
        if self._on_error is None:
            return
        self._on_error(ex)

    def complete(self):
        if self._on_complete is None:
            return

        self._on_complete()
