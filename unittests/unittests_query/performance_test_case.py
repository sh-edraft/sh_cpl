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
        default = timeit.timeit(lambda: list(range(0, VALUES)), number=COUNT)
        iterable = timeit.timeit(lambda: Iterable.range(0, VALUES), number=COUNT)
        enumerable = timeit.timeit(lambda: Enumerable.range(0, VALUES), number=COUNT)

        print('Range')
        print(f'd: {default}s')
        print(f'i: {iterable}s')
        print(f'e: {enumerable}s')

        self.assertAlmostEqual(round(default, 3), round(enumerable, 3))
        self.assertAlmostEqual(round(default, 3), round(iterable, 3))

    def test_where_single(self):
        default = timeit.timeit(lambda: [x for x in list(range(0, VALUES)) if x == 50], number=COUNT)
        iterable = timeit.timeit(lambda: Iterable.range(0, VALUES).where(lambda x: x == 50).single(), number=COUNT)
        enumerable = timeit.timeit(lambda: Enumerable.range(0, VALUES).where(lambda x: x == 50).single(), number=COUNT)

        print('Where single')
        print(f'd: {default}s')
        print(f'i: {iterable}s')
        print(f'e: {enumerable}s')

        self.assertLess(default, enumerable)
        self.assertLess(default, iterable)

    def test_where_single_complex(self):
        class TestModel:

            def __init__(self, v, tm=None):
                self.value = v
                self.tm = tm

        values = []
        for i in range(VALUES):
            values.append(TestModel(i, TestModel(i + 1)))

        default = timeit.timeit(lambda: [x for x in values if x.tm.value == 50], number=COUNT)
        iterable = timeit.timeit(lambda: Iterable(TestModel, values).where(lambda x: x.tm.value == 50).single(), number=COUNT)
        enumerable = timeit.timeit(lambda: Enumerable(TestModel, values).where(lambda x: x.tm.value == 50).single(), number=COUNT)

        print('Complex where single')
        print(f'd: {default}s')
        print(f'i: {iterable}s')
        print(f'e: {enumerable}s')

        self.assertLess(default, enumerable)
        self.assertLess(default, iterable)
