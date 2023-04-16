import time
import unittest
from datetime import datetime

from cpl_core.console import Console
from cpl_reactive_extensions.scheduler.async_scheduler import async_scheduler
from cpl_reactive_extensions.timer import Timer


class SchedulerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_timer(self):
        count = 0

        def task():
            nonlocal count
            Console.write_line(datetime.now(), "Hello world")
            count += 1

        timer = Timer(100, task)
        time.sleep(0.25)
        self.assertEqual(count, 2)
        timer.clear()

    def test_schedule(self):
        count = 0

        def task():
            nonlocal count
            Console.write_line(datetime.now(), "Hello world")
            count += 1

        async_scheduler.schedule(task, 100)
        time.sleep(2)
