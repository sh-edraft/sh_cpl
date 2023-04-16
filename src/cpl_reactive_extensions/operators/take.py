from cpl_core.type import T
from cpl_reactive_extensions import Subscriber, Observable
from cpl_reactive_extensions.operator_subscriber import OperatorSubscriber
from cpl_reactive_extensions.utils import operate


def take(count: int):
    if count <= 0:
        return Observable()

    def init(source: Observable, subscriber: Subscriber):
        seen = 0

        def sub(value: T):
            nonlocal seen

            if seen + 1 <= count:
                seen += 1
                subscriber.next(value)

                if count <= seen:
                    subscriber.complete()

        source.subscribe(OperatorSubscriber(subscriber, sub))

    return operate(init)
