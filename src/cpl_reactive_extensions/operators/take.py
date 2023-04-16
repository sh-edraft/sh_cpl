from cpl_core.type import T
from cpl_reactive_extensions.internal.subscriber import Subscriber
from cpl_reactive_extensions.observable import Observable
from cpl_reactive_extensions.internal.operator_subscriber import OperatorSubscriber
from cpl_reactive_extensions.internal.utils import operate


def take(count: int):
    if count <= 0:
        return Observable()

    def init(source: Observable, subscriber: Subscriber):
        seen = 0

        def on_next(value: T):
            nonlocal seen

            if seen + 1 <= count:
                seen += 1
                subscriber.next(value)

                if count <= seen:
                    subscriber.complete()
            else:
                sub.unsubscribe()

        sub = source.subscribe(OperatorSubscriber(subscriber, on_next))

    return operate(init)
