from __future__ import annotations

from typing import Union, Callable, Optional

from cpl_reactive_extensions.abc.unsubscribable import Unsubscribable


class Subscription(Unsubscribable):
    def __init__(self, initial_teardown: Optional[Callable] = None):
        Unsubscribable.__init__(self)

        self._initial_teardown = initial_teardown

        self._closed = False
        self._subscriptions = []

        self._parentage: list[Subscription] = []
        self._finalizers: list[Subscription] = []

    @property
    def closed(self) -> bool:
        return self._closed

    def _add_parent(self, parent: Subscription):
        self._parentage.append(parent)

    def _has_parent(self, parent: Subscription) -> bool:
        return parent in self._parentage

    def _exec_finalizer(self, finalizer: Union[Callable, Unsubscribable]):
        if isinstance(finalizer, Callable):
            finalizer()
        else:
            finalizer.unsubscribe()

    def unsubscribe(self):
        if not self._closed:
            self._closed = True

        for parent in self._parentage:
            parent.remove(self)

        if self._initial_teardown is not None:
            try:
                self._initial_teardown()
            except Exception as e:
                print(e)

        for finalizer in self._finalizers:
            try:
                self._exec_finalizer(finalizer)
            except Exception as e:
                print(e)

        self._subscriptions.clear()

    def add(self, tear_down: Union[Subscription, Unsubscribable]):
        if tear_down is None or tear_down == self:
            return

        if self.closed:
            self._exec_finalizer(tear_down)
            return

        if isinstance(tear_down, Subscription):
            if tear_down.closed or tear_down._has_parent(self):
                return

            tear_down._add_parent(self)

        self._subscriptions.append(tear_down)

    def remove(self, tear_down: Union[Subscription, Unsubscribable]):
        self._subscriptions.remove(tear_down)
