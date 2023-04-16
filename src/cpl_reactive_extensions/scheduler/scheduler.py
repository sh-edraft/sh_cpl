from datetime import datetime
from typing import Callable, Optional, Type

from cpl_core.type import T, Number
from cpl_reactive_extensions.abc.scheduler_action import SchedulerAction
from cpl_reactive_extensions.abc.scheduler_like import SchedulerLike
from cpl_reactive_extensions.internal.action import Action
from cpl_reactive_extensions.internal.subscription import Subscription


class Scheduler(SchedulerLike):
    @staticmethod
    @property
    def _get_now(self=None) -> Number:
        return int(datetime.now().strftime("%s"))

    now = _get_now

    def __init__(self, scheduler_action_ctor: Type[Action], now=None):
        self.now = self._get_now if now is None else now
        self._scheduler_action_ctor = scheduler_action_ctor

    def schedule(
        self, work: Callable[[SchedulerAction, Optional[T]], None], delay: Number, state: T = None
    ) -> Subscription:
        action = self._scheduler_action_ctor(self, work)
        x = action.schedule(state, delay)

        return x
