import sys
import timeit
import unittest

from cpl_query.enumerable import Enumerable
from cpl_query.iterable import Iterable

VALUES = 10000
COUNT = 50


class PerformanceTestCase(unittest.TestCase):

    def setUp(self):
        i = 0
        self.values = []
        while i < VALUES:
            self.values.append(i)
            i += 1

    def test_range(self):
        default = timeit.timeit(lambda: list(self.values), number=COUNT)
        enumerable = timeit.timeit(lambda: Enumerable(int, self.values), number=COUNT)
        iterable = timeit.timeit(lambda: Iterable(int, self.values), number=COUNT)

        print('Range')
        print(f'd: {default}')
        print(f'i: {iterable}')
        print(f'e: {enumerable}')

        self.assertLess(default, enumerable)
        self.assertLess(default, iterable)

    def test_where_single(self):
        default = timeit.timeit(lambda: [x for x in list(self.values) if x == 50], number=COUNT)
        iterable = timeit.timeit(lambda: Iterable(int, self.values).where(lambda x: x == 50).single(), number=COUNT)
        enumerable = timeit.timeit(lambda: Enumerable(int, self.values).where(lambda x: x == 50).single(), number=COUNT)

        print('Where single')
        print(f'd: {default}')
        print(f'i: {iterable}')
        print(f'e: {enumerable}')

        self.assertLess(default, enumerable)
        self.assertLess(default, iterable)
