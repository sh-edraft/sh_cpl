from typing import Optional

from cpl_core.type import T, Number
from cpl_reactive_extensions.abc.scheduler_action import SchedulerAction
from cpl_reactive_extensions.internal.operator_subscriber import OperatorSubscriber
from cpl_reactive_extensions.internal.subscriber import Subscriber
from cpl_reactive_extensions.internal.subscription import Subscription
from cpl_reactive_extensions.internal.utils import operate
from cpl_reactive_extensions.observable import Observable
from cpl_reactive_extensions.scheduler.async_scheduler import async_scheduler


def debounce_time(time: Number, scheduler=async_scheduler):
    def init(source: Observable, subscriber: Subscriber):
        active_task: Optional[Subscription] = None
        last_value: Optional[T] = None
        last_time: Optional[Number] = None

        def emit():
            nonlocal active_task, last_value

            if active_task is None:
                return

            active_task.unsubscribe()
            active_task = None
            value = last_value
            last_value = None
            subscriber.next(value)

        def emit_when_idle(action: SchedulerAction):
            nonlocal active_task, last_time
            target_time = last_time + time
            now = scheduler.now

            if now < target_time:
                active_task = action.schedule(None, target_time - now)
                subscriber.add(active_task)
                return

            emit()

        def on_next(value: T):
            nonlocal active_task, last_value
            last_value = value

            if active_task is None:
                active_task = scheduler.schedule(emit_when_idle, time)
                subscriber.add(active_task)

        def on_complete():
            emit()
            subscriber.complete()

        def on_finalize():
            nonlocal active_task, last_value
            last_value = None
            active_task = None

        sub = source.subscribe(OperatorSubscriber(subscriber, on_next, None, on_complete, on_finalize))

    return operate(init)
