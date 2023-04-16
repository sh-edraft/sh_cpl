import time
import traceback
import unittest

from cpl_core.console import Console
from cpl_reactive_extensions.observable import Observable
from cpl_reactive_extensions.operators import debounce_time
from cpl_reactive_extensions.subject.subject import Subject
from cpl_reactive_extensions.interval import Interval
from cpl_reactive_extensions.operators.take import take
from cpl_reactive_extensions.operators.take_until import take_until


class ObservableOperatorTestCase(unittest.TestCase):
    def setUp(self):
        self._error = False
        self._completed = False

    def _on_error(self, ex: Exception):
        tb = traceback.format_exc()
        Console.error(f"Got error from observable: {ex}", tb)
        self._error = True

    def _on_complete(self):
        self._completed = True

    def test_take_two(self):
        count = 0

        def sub(x):
            nonlocal count

            count += 1

        observable = Interval(0.1)
        observable.pipe(take(2)).subscribe(sub)
        time.sleep(0.5)
        self.assertEqual(count, 2)

    def test_take_five(self):
        count = 0

        def sub(x):
            nonlocal count

            count += 1

        observable = Interval(0.1)
        observable.pipe(take(5)).subscribe(sub)
        time.sleep(1)
        self.assertEqual(count, 5)

    def test_take_until(self):
        count = 0
        unsubscriber = Subject(None)

        def sub(x):
            nonlocal count

            count += 1

        observable = Interval(0.1)
        observable.pipe(take_until(unsubscriber)).subscribe(sub)

        timer = 2
        time.sleep(timer)
        unsubscriber.next(None)
        unsubscriber.complete()
        self.assertEqual(count, timer * 10 - 1)

    def test_debounce_time(self):
        def call(x):
            x.next(1)
            x.next(2)
            x.next(3)
            x.next(4)
            x.next(5)
            x.next(6)
            x.complete()

        observable = Observable(call)

        observable.pipe(debounce_time(600)).subscribe(lambda x: Console.write_line("Hey", x))
