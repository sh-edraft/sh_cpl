import threading
import time
from typing import Callable

from cpl_core.type import Number


class Timer:
    def __init__(self, interval: Number, action: Callable, *args):
        self._interval = interval / 1000
        self._action = action
        self._args = args
        self.stop_event = threading.Event()
        thread = threading.Thread(target=self.__set_interval)
        thread.start()

    def __set_interval(self):
        next_time = time.time() + self._interval
        while not self.stop_event.wait(next_time - time.time()):
            next_time += self._interval
            self._action(*self._args)

    def clear(self):
        self.stop_event.set()
