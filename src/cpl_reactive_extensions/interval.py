import sched
import threading
import time
from typing import Callable

from cpl_reactive_extensions.observable import Observable
from cpl_reactive_extensions.subscriber import Subscriber


class Interval(Observable):
    def __init__(self, interval: float, callback: Callable = None):
        self._interval = interval
        callback = callback if callback is not None else self._default_callback

        def schedule(x: Subscriber):
            scheduler = sched.scheduler(time.time, time.sleep)
            scheduler.enter(
                self._interval,
                1,
                self._run,
                (scheduler, x, callback),
            )
            scheduler.run()

        def thread(x: Subscriber):
            t = threading.Thread(target=schedule, args=(x,))
            t.start()

        Observable.__init__(self, thread)
        self._i = 0

    def _run(self, scheduler, x: Subscriber, callback: Callable):
        if x.closed:
            x.complete()
            return

        scheduler.enter(
            self._interval,
            1,
            self._run,
            (scheduler, x, callback),
        )
        callback(x)

    def _default_callback(self, x: Subscriber):
        x.next(self._i)
        self._i += 1
