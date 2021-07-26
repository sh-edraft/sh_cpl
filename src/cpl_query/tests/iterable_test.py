import unittest

from cpl_query.extension.list import List


class IterableTest(unittest.TestCase):

    def setUp(self) -> None:
        self._list = List(int)

    def _clear(self):
        self._list.clear()
        self.assertEqual(self._list, [])

    def test_append(self):
        self._list.append(1)
        self._list.append(2)
        self._list.append(3)

        self.assertEqual(self._list, [1, 2, 3])
        self._clear()

    def test_append_wrong_type(self):
        self._list.append(1)
        self._list.append(2)

        self.assertRaises(Exception, lambda v: self._list.append(v), '3')
        self._clear()
