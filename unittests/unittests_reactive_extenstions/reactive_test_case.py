import unittest
from threading import Timer

from cpl_reactive_extensions.observable import Observable
from cpl_reactive_extensions.observer import Observer


class ReactiveTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_observer(self):
        called = 0
        has_error = False
        completed = False
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

        def on_err():
            nonlocal has_error
            has_error = True

        def on_complete():
            nonlocal completed
            completed = True

        self.assertEqual(called, 0)
        self.assertFalse(has_error)
        self.assertFalse(completed)
        observable.subscribe(
            Observer(
                on_next,
                on_err,
                on_complete,
            )
        )
        self.assertEqual(called, 3)
        self.assertFalse(has_error)
        self.assertFalse(completed)

        def complete():
            self.assertEqual(called, 4)
            self.assertFalse(has_error)
            self.assertTrue(completed)

        Timer(1.0, complete).start()

    def test_subject(self):
        pass
