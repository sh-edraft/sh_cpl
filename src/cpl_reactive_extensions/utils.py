from typing import Callable

from cpl_reactive_extensions import Observable, Subscriber


def operate(init: Callable[[Observable, Subscriber], None]):
    def observable(source: Observable):
        def create(self: Subscriber, lifted_source: Observable):
            try:
                return init(lifted_source, self)
            except Exception as e:
                self.error(e)

        if "lift" not in dir(source):
            raise TypeError("Unable to lift unknown Observable type")

        return source.lift(create)

    return observable
