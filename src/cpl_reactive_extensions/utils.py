from typing import Callable

from cpl_reactive_extensions import Observable, Subscriber
from cpl_reactive_extensions.abc import Operator


def operate(init: Callable[[Observable, Subscriber], Operator]):
    def observable(source: Observable):
        def create(self: Subscriber, lifted_source: Observable):
            try:
                return init(lifted_source, self)
            except Exception as e:
                self.error(e)

        operator = Operator()
        operator.call = create

        if "lift" not in dir(source):
            raise TypeError("Unable to lift unknown Observable type")

        return source.lift(operator)

    return observable
