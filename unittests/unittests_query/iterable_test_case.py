import unittest

from cpl_query.extension.list import List


class IterableTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._list = List(int)

    def _clear(self):
        self._list.clear()
        self.assertEqual(self._list, [])

    def test_append(self):
        self._list.append(1)
        self._list.append(2)
        self._list.append(3)

        self.assertEqual(self._list.to_list(), [1, 2, 3])
        self.assertRaises(Exception, lambda v: self._list.append(v), '3')

    def test_assign(self):
        self._list.append(1)
        self._list.append(2)
        self._list.append(3)
        self._list[0] = 42
        self.assertEqual(self._list[0], 42)
        self._list[0] = 1
        self._list.append(42)
        self.assertEqual(self._list[3], 42)
        del self._list[3]

        self.assertEqual(self._list.to_list(), [1, 2, 3])
        self.assertRaises(Exception, lambda v: self._list.append(v), '3')
