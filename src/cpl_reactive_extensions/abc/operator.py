from abc import ABC
from typing import Any

from cpl_reactive_extensions.subscriber import Subscriber


class Operator(ABC):
    def __init__(self):
        ABC.__init__(self)

    def call(self, subscriber: Subscriber, source: Any):
        pass
