import unittest

from unittests_reactive_extenstions.observable_operator import ObservableOperatorTestCase
from unittests_reactive_extenstions.reactive_test_case import ReactiveTestCase


class ReactiveTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self.addTests(loader.loadTestsFromTestCase(ReactiveTestCase))
        self.addTests(loader.loadTestsFromTestCase(ObservableOperatorTestCase))

    def run(self, *args):
        super().run(*args)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(ReactiveTestSuite())
