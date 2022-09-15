import unittest

from cpl_query.enumerable.enumerable import Enumerable


class EnumerableTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._list = Enumerable(int)

    def _clear(self):
        self._list.clear()
        self.assertEqual(self._list, [])

    def test_append(self):
        self._list.add(1)
        self._list.add(2)
        self._list.add(3)

        self.assertEqual(self._list.to_list(), [1, 2, 3])
        self.assertRaises(Exception, lambda v: self._list.add(v), '3')

    def test_default(self):
        self.assertEqual(Enumerable.empty().to_list(), [])
        self.assertEqual(Enumerable.range(0, 100).to_list(), list(range(0, 100)))

    def test_iter(self):
        n = 0
        elements = Enumerable.range(0, 100)
        while n < 100:
            self.assertEqual(elements.next(), n)
            n += 1

    def test_for(self):
        n = 0
        for i in Enumerable.range(0, 100):
            self.assertEqual(i, n)
            n += 1

    def test_get(self):
        self._list.add(1)
        self._list.add(2)
        self._list.add(3)

        self.assertEqual(self._list.element_at(2), [1, 2, 3][2])

    def test_count(self):
        self._list.add(1)
        self._list.add(2)
        self._list.add(3)

        self.assertEqual(self._list.count(), 3)

    def test_remove(self):
        old_values = self._list._values
        self._list.add(1)
        self.assertNotEqual(old_values, self._list._values)
        self._list.add(2)
        self._list.add(3)

        self.assertEqual(self._list.to_list(), [1, 2, 3])
        self.assertRaises(Exception, lambda v: self._list.add(v), '3')
        old_values = self._list._values
        self._list.remove(3)
        self.assertNotEqual(old_values, self._list._values)
        self.assertEqual(self._list.to_list(), [1, 2])
        self.assertRaises(Exception, lambda v: self._list.add(v), '3')
