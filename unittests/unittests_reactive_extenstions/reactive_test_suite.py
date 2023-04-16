import unittest

from unittests_reactive_extenstions.observable_operator_test_case import ObservableOperatorTestCase
from unittests_reactive_extenstions.reactive_test_case import ReactiveTestCase
from unittests_reactive_extenstions.scheduler_test_case import SchedulerTestCase


class ReactiveTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self.addTests(loader.loadTestsFromTestCase(ReactiveTestCase))
        self.addTests(loader.loadTestsFromTestCase(ObservableOperatorTestCase))
        self.addTests(loader.loadTestsFromTestCase(SchedulerTestCase))

    def run(self, *args):
        super().run(*args)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(ReactiveTestSuite())
