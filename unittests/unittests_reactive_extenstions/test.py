import time
from datetime import datetime

from cpl_core.console import Console
from cpl_reactive_extensions.timer import Timer


def test_timer():
    is_working = False

    def task():
        nonlocal is_working
        Console.write_line(datetime.now(), "Hello world")
        is_working = True

    timer = Timer(100, task)
    time.sleep(0.2)
    timer.clear()


test_timer()
