import traceback
import unittest
from threading import Timer

from cpl_core.console import Console
from cpl_reactive_extensions.observable import Observable
from cpl_reactive_extensions.observer import Observer
from cpl_reactive_extensions.subject import Subject


class ReactiveTestCase(unittest.TestCase):
    def setUp(self):
        self._error = False
        self._completed = False

    def _on_error(self, ex: Exception):
        tb = traceback.format_exc()
        Console.error(f"Somthing went wrong: {ex}", tb)
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

        def _next(x):
            nonlocal expected_x
            self.assertEqual(expected_x, x)
            expected_x += 1
            if expected_x == 4:
                expected_x = 1

        subject = Subject(int)
        subject.subscribe(_next, self._on_error, self._on_complete)
        subject.subscribe(_next, self._on_error, self._on_complete)

        observable = Observable.from_list([1, 2, 3])
        observable.subscribe(subject, self._on_error, self._on_complete)

        self.assertFalse(self._error)
