from typing import Any

from cpl_reactive_extensions.subscriber import Subscriber


class Operator:
    def call(self, subscriber: Subscriber, source: Any):
        pass
