from typing import Callable

from cpl_core.type import Number
from cpl_reactive_extensions.timer import Timer


class TimerProvider:
    @staticmethod
    def set_timer(handler: Callable, timeout: Number = None, *args):
        return Timer(timeout, handler, *args)
