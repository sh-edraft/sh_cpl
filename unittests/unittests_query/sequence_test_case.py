import unittest

from cpl_query.enumerable import Enumerable
from cpl_query.extension.list import List
from cpl_query.iterable import Iterable


class SequenceTestCase(unittest.TestCase):

    def test_to_list(self):
        _list = List().extend(range(0, 100))
        enumerable = Enumerable.range(0, 100)
        iterable = Iterable(int, list(range(0, 100)))

        self.assertEqual(enumerable.to_list(), _list.to_list())
        self.assertEqual(iterable.to_list(), _list.to_list())

    def test_to_enumerable(self):
        _list = List().extend(range(0, 100))
        enumerable = Enumerable.range(0, 100)
        iterable = Iterable(int, list(range(0, 100)))

        self.assertEqual(type(_list.to_enumerable()), type(enumerable))
        self.assertEqual(type(iterable.to_enumerable()), type(enumerable))

    def test_to_iterable(self):
        _list = List().extend(range(0, 100))
        enumerable = Enumerable.range(0, 100)
        iterable = Iterable(int, list(range(0, 100)))

        self.assertEqual(type(_list.to_iterable()), type(iterable))
        self.assertEqual(type(enumerable.to_iterable()), type(iterable))
