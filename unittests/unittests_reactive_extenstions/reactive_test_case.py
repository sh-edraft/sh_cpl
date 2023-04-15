import time
import traceback
import unittest
from datetime import datetime
from threading import Timer

from cpl_core.console import Console
from cpl_reactive_extensions.behavior_subject import BehaviorSubject
from cpl_reactive_extensions.interval import Interval
from cpl_reactive_extensions.observable import Observable
from cpl_reactive_extensions.subject import Subject
from cpl_reactive_extensions.subscriber import Observer


class ReactiveTestCase(unittest.TestCase):
    def setUp(self):
        self._error = False
        self._completed = False

    def _on_error(self, ex: Exception):
        tb = traceback.format_exc()
        Console.error(f"Got error from observable: {ex}", tb)
        self._error = True

    def _on_complete(self):
        self._completed = True

    def test_observer(self):
        called = 0
        test_x = 1

        def callback(observer: Observer):
            nonlocal test_x
            observer.next(test_x)
            test_x += 1
            observer.next(test_x)
            test_x += 1
            observer.next(test_x)

            def complete():
                nonlocal test_x
                test_x += 1
                observer.next(test_x)
                observer.complete()

            Timer(1.0, complete).start()

        observable = Observable(callback)

        def on_next(x):
            nonlocal called
            called += 1
            self.assertEqual(test_x, x)

        self.assertEqual(called, 0)
        self.assertFalse(self._error)
        self.assertFalse(self._completed)
        observable.subscribe(
            on_next,
            self._on_error,
            self._on_complete,
        )
        self.assertEqual(called, 3)
        self.assertFalse(self._error)
        self.assertFalse(self._completed)

        def complete():
            self.assertEqual(called, 4)
            self.assertFalse(self._error)
            self.assertTrue(self._completed)

        Timer(1.0, complete).start()

        time.sleep(2)

        def _test_complete(x: Observer):
            x.next(1)
            x.next(2)
            x.complete()
            x.next(3)

        observable2 = Observable(_test_complete)

        observable2.subscribe(lambda x: x, self._on_error)
        self.assertTrue(self._error)

    def test_observable_from(self):
        expected_x = 1

        def _next(x):
            nonlocal expected_x
            self.assertEqual(expected_x, x)
            expected_x += 1

        observable = Observable.from_list([1, 2, 3, 4])
        observable.subscribe(
            _next,
            self._on_error,
        )
        self.assertFalse(self._error)

    def test_subject(self):
        expected_x = 1

        def _next(calc, x):
            nonlocal expected_x
            self.assertEqual(expected_x, x)
            if not calc:
                return
            expected_x += 1
            if expected_x == 4:
                expected_x = 1

        subject = Subject(int)
        subject.subscribe(lambda x: _next(False, x), self._on_error)
        subject.subscribe(lambda x: _next(True, x), self._on_error)

        observable = Observable.from_list([1, 2, 3])
        observable.subscribe(subject, self._on_error)

        self.assertFalse(self._error)

    def test_behavior_subject(self):
        subject = BehaviorSubject(int, 0)

        subject.subscribe(lambda x: Console.write_line("a", x))

        subject.next(1)
        subject.next(2)

        subject.subscribe(lambda x: Console.write_line("b", x))
        subject.next(3)

    def test_interval_default(self):
        wait = 10
        i = 0

        def test_sub(x):
            nonlocal i
            self.assertEqual(x, i)
            i += 1

        observable = Interval(1.0)
        sub = observable.subscribe(test_sub)
        start = datetime.now()

        time.sleep(wait)
        sub.unsubscribe()
        end = datetime.now()
        self.assertEqual(round((end - start).total_seconds()), wait)
