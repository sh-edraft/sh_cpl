from typing import Optional

from cpl_core.type import T, Number
from cpl_reactive_extensions.internal.action import Action
from cpl_reactive_extensions.internal.subscription import Subscription
from cpl_reactive_extensions.timer import Timer


class AsyncAction(Action):
    def __init__(self, scheduler, work):
        from cpl_reactive_extensions.scheduler.async_scheduler import AsyncScheduler

        Action.__init__(self, scheduler, work)

        self._scheduler: AsyncScheduler = scheduler
        self._work = work

        self.timer = None
        self.state: Optional[T] = None
        self.delay: Number = 0
        self._pending = False

    def schedule(self, state: T = None, delay: Number = 0) -> Subscription:
        if self.closed:
            return self

        self.state = state

        timer = self.timer
        scheduler = self._scheduler

        if timer is not None:
            self.timer = self.recycle_async_timer(scheduler, timer, delay)

        self._pending = True
        self.delay = delay
        self.timer = self.timer if self.timer is not None else self.request_async_timer(scheduler, delay)

        return self

    def request_async_timer(self, scheduler, delay: Number = 0):
        from cpl_reactive_extensions.scheduler.async_scheduler import AsyncScheduler

        scheduler: AsyncScheduler = scheduler
        return Timer(delay, lambda: scheduler.flush(self))

    def recycle_async_timer(self, scheduler, timer=None, delay: Number = None):
        from cpl_reactive_extensions.scheduler.async_scheduler import AsyncScheduler

        scheduler: AsyncScheduler = scheduler
        if delay is None and self.delay == delay and not self._pending:
            return timer

        if timer is not None:
            timer.clear()

        return None

    def execute(self, state: T, delay: Number):
        if self.closed:
            return Exception("Executing cancelled action")

        self._pending = False
        error = self._execute(state, delay)
        if error is not None:
            return error
        elif not self._pending and self.timer is not None:
            self._timer = self.recycle_async_timer(self._scheduler, self.timer, None)

    def _execute(self, state: T, delay: Number):
        errored = False
        ex = None
        try:
            self._work(state)
        except Exception as e:
            errored = True
            ex = e

        if errored:
            self.unsubscribe()
            return ex

    def unsubscribe(self):
        if self.closed:
            return

        self._scheduler.actions.remove(self)

        if self._timer is not None:
            self._timer = self.recycle_async_timer(self._scheduler, self.timer, None)

        self._work = None
        self.state = None
        self._scheduler = None
        self._pending = False
        self.delay = None
        Action.unsubscribe(self)
