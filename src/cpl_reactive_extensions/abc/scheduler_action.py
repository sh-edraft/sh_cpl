from abc import ABC, abstractmethod

from cpl_core.type import T, Number
from cpl_reactive_extensions.internal.subscription import Subscription


class SchedulerAction(ABC):
    @abstractmethod
    def schedule(self, state: T = None, delay: Number = None) -> Subscription:
        pass
