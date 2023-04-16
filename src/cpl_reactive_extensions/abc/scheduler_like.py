from abc import ABC, abstractmethod
from typing import Callable, Optional

from cpl_core.type import Number, T
from cpl_reactive_extensions.internal.subscription import Subscription
from cpl_reactive_extensions.abc.scheduler_action import SchedulerAction


class SchedulerLike(ABC):
    @abstractmethod
    def schedule(self, work: Callable[[SchedulerAction, Optional[T]], None], delay: Number, state: T) -> Subscription:
        pass
