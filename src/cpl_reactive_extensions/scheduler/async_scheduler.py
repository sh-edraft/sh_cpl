from typing import Type

from cpl_reactive_extensions.internal.action import Action
from cpl_reactive_extensions.internal.async_action import AsyncAction
from cpl_reactive_extensions.scheduler.scheduler import Scheduler


class AsyncScheduler(Scheduler):
    def __init__(self, scheduler_action_ctor: Type[Action], now=None):
        Scheduler.__init__(self, scheduler_action_ctor, now)

        self.actions: list[AsyncAction] = []
        self._active = False

    def flush(self, action: AsyncAction):
        if self._active:
            self.actions.append(action)
            return

        error = None
        self._active = True

        for action in self.actions:
            error = action.execute(action.state, action.delay)
            if error:
                break

        self._active = False

        if error is not None:
            for action in self.actions:
                action.unsubscribe()
            raise error


async_scheduler = AsyncScheduler(AsyncAction)
