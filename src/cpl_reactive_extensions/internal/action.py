from cpl_core.type import T, Number
from cpl_reactive_extensions.internal.subscription import Subscription


class Action(Subscription):
    def __init__(self, scheduler, work):
        Subscription.__init__(self)

    def schedule(self, state: T = None, delay: Number = 0) -> Subscription:
        return self
