from cpl_core.type import T
from cpl_reactive_extensions import Subscriber, Observable
from cpl_reactive_extensions.operator_subscriber import OperatorSubscriber
from cpl_reactive_extensions.utils import operate


def take_until(notifier: Observable):
    def init(source: Observable, subscriber: Subscriber):
        Observable.from_observable(notifier).subscribe(OperatorSubscriber(subscriber, lambda: subscriber.complete()))

        if not subscriber.closed:
            source.subscribe(subscriber)

    return operate(init)
