from cpl_reactive_extensions.observable import Observable
from cpl_reactive_extensions.internal.operator_subscriber import OperatorSubscriber
from cpl_reactive_extensions.internal.subscriber import Subscriber
from cpl_reactive_extensions.internal.utils import operate


def take_until(notifier: Observable):
    def init(source: Observable, subscriber: Subscriber):
        Observable.from_observable(notifier).subscribe(OperatorSubscriber(subscriber, lambda: subscriber.complete()))

        if not subscriber.closed:
            source.subscribe(subscriber)

    return operate(init)
