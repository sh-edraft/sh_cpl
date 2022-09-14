import sys
import timeit
import unittest

from cpl_query.enumerable import Enumerable
from cpl_query.extension.list import List
from cpl_query.iterable import Iterable

VALUES = 1000
COUNT = 100


class PerformanceTestCase(unittest.TestCase):

    def setUp(self):
        i = 0
        self.values = []
        while i < VALUES:
            self.values.append(i)
            i += 1

    # def test_range(self):
    #     default = timeit.timeit(lambda: list(self.values), number=COUNT)
    #     enumerable = timeit.timeit(lambda: Enumerable(int, self.values), number=COUNT)
    #     iterable = timeit.timeit(lambda: Iterable(int, self.values), number=COUNT)
    #
    #     print(f'd: {default}')
    #     print(f'e: {enumerable}')
    #     print(f'i: {iterable}')
    #
    #     self.assertLess(default, enumerable)
    #     self.assertLess(default, iterable)

    def test_where_single(self):
        print(Enumerable(int, self.values).where(lambda x: x == COUNT).single_or_default())
        # default = timeit.timeit(lambda: [x for x in list(self.values) if x == 50], number=COUNT)
        # enumerable = timeit.timeit(lambda: Enumerable(int, self.values).where(lambda x: x == 50).single(), number=COUNT)
        # iterable = timeit.timeit(lambda: Iterable(int, self.values).where(lambda x: x == 50).single(), number=COUNT)
        #
        # print(f'd: {default}')
        # print(f'e: {enumerable}')
        # print(f'i: {iterable}')
        #
        # self.assertLess(default, enumerable)
        # self.assertLess(default, iterable)
