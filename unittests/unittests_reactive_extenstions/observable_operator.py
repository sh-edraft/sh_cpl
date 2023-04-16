import traceback
import unittest

from cpl_core.console import Console
from cpl_reactive_extensions.interval import Interval
from cpl_reactive_extensions.operators.take import take


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
        def sub(x):
            Console.write_line(x)

        observable = Interval(1.0)
        sub = observable.pipe(take(2)).subscribe(sub)
