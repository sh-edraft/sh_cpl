import string
import unittest
from random import randint

from cpl_core.utils import String
from cpl_query.exceptions import InvalidTypeException, ArgumentNoneException
from cpl_query.extension.list import List
from unittests_query.models import User, Address


class IterableQueryTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._tests = List(User)
        self._t_user = User(
            'Test user',
            Address(
                'teststr.',
                15
            )
        )
        self._t_user2 = User(
            'Test user',
            Address(
                'teststr.',
                14
            )
        )

        self._generate_test_data()

    def _generate_test_data(self):
        for i in range(0, 100):
            user = User(
                String.random_string(string.ascii_letters, 8).lower(),
                Address(
                    String.random_string(string.ascii_letters, 10).lower(),
                    randint(1, 10)
                )
            )

            self._tests.append(user)

        self._tests.append(self._t_user)
        self._tests.append(self._t_user2)

    def test_any(self):
        results = []
        for user in self._tests:
            if user.address.nr == 10:
                results.append(user)

        res = self._tests.any(lambda u: u.address.nr == 10)
        n_res = self._tests.any(lambda u: u.address.nr == 100)

        self.assertTrue(res)
        self.assertFalse(n_res)

    def test_all(self):
        results = []
        for user in self._tests:
            if user.address.nr == 10:
                results.append(user)

        res = self._tests.all(lambda u: u.address is not None)
        n_res = self._tests.all(lambda u: u.address.nr == 100)

        self.assertTrue(res)
        self.assertFalse(n_res)

    def test_avg(self):
        avg = 0
        for user in self._tests:
            avg += user.address.nr

        avg = avg / len(self._tests)
        res = self._tests.average(lambda u: u.address.nr)

        self.assertEqual(avg, res)

        def invalid():
            tests = List(str, ['hello', 'world'])
            e_res = tests.average()

        self.assertRaises(InvalidTypeException, invalid)

        tests = List(int, list(range(0, 100)))
        self.assertEqual(sum(tests) / len(tests), tests.average())

        def wrong2():
            tests2 = List(int, values=list(range(0, 100)))
            e_res = tests2.average(lambda u: u.address.nr)

        self.assertRaises(AttributeError, wrong2)

    def test_contains(self):
        self.assertTrue(self._tests.contains(self._t_user))
        self.assertFalse(self._tests.contains(User("Test", None)))

    def test_count(self):
        self.assertEqual(len(self._tests), self._tests.count())
        self.assertEqual(1, self._tests.count(lambda u: u == self._t_user))

    def test_distinct(self):
        res = self._tests.distinct(lambda u: u.address.nr).where(lambda u: u.address.nr == 5)
        self.assertEqual(1, len(res))

    def test_element_at(self):
        index = randint(0, len(self._tests) - 1)
        self.assertEqual(self._tests[index], self._tests.element_at(index))

    def test_element_at_or_default(self):
        index = randint(0, len(self._tests) - 1)
        self.assertEqual(self._tests[index], self._tests.element_at_or_default(index))
        self.assertIsNone(self._tests.element_at_or_default(len(self._tests)))

    def test_last(self):
        results = []
        for user in self._tests:
            if user.address.nr == 10:
                results.append(user)

        res = self._tests.where(lambda u: u.address.nr == 10)
        s_res = self._tests.where(lambda u: u.address.nr == 10).last()

        self.assertEqual(len(res), len(results))
        self.assertEqual(res[len(res) - 1], s_res)

    def test_last_or_default(self):
        results = []
        for user in self._tests:
            if user.address.nr == 10:
                results.append(user)

        res = self._tests.where(lambda u: u.address.nr == 10)
        s_res = self._tests.where(lambda u: u.address.nr == 10).last_or_default()
        sn_res = self._tests.where(lambda u: u.address.nr == 11).last_or_default()

        self.assertEqual(len(res), len(results))
        self.assertEqual(res[len(res) - 1], s_res)
        self.assertIsNone(sn_res)

    def test_first(self):
        results = []
        for user in self._tests:
            if user.address.nr == 10:
                results.append(user)

        res = self._tests.where(lambda u: u.address.nr == 10)
        s_res = self._tests.where(lambda u: u.address.nr == 10).first()

        self.assertEqual(len(res), len(results))
        self.assertEqual(res[0], s_res)
        self.assertEqual(res[0], res.first())
        self.assertEqual(res.first(), res.first())

    def test_first_or_default(self):
        results = []
        for user in self._tests:
            if user.address.nr == 10:
                results.append(user)

        res = self._tests.where(lambda u: u.address.nr == 10)
        s_res = self._tests.where(lambda u: u.address.nr == 10).first_or_default()
        sn_res = self._tests.where(lambda u: u.address.nr == 11).first_or_default()

        self.assertEqual(len(res), len(results))
        self.assertEqual(res[0], s_res)
        self.assertIsNone(sn_res)

    def test_for_each(self):
        users = []
        self._tests.for_each(lambda user: (
            users.append(user)
        )
                             )

        self.assertEqual(len(users), len(self._tests))

    def test_max(self):
        res = self._tests.max(lambda u: u.address.nr)
        self.assertEqual(res, self._t_user.address.nr)

        tests = List(int, list(range(0, 100)))
        self.assertEqual(99, tests.max())

        def invalid():
            tests = List(str, ['hello', 'world'])
            e_res = tests.average()

        self.assertRaises(InvalidTypeException, invalid)

    def test_min(self):
        res = self._tests.min(lambda u: u.address.nr)
        self.assertEqual(1, res)

        tests = List(int, list(range(0, 100)))
        self.assertEqual(0, tests.min())

        def invalid():
            tests = List(str, ['hello', 'world'])
            e_res = tests.average()

        self.assertRaises(InvalidTypeException, invalid)

    def test_order_by(self):
        res = self._tests.order_by(lambda user: user.address.street)
        res2 = self._tests.order_by(lambda user: user.address.nr).to_list()
        s_res = self._tests.to_list()
        s_res.sort(key=lambda user: user.address.street)
        self.assertEqual(res.to_list(), s_res)

        s_res = self._tests.to_list()
        s_res.sort(key=lambda user: user.address.nr)
        self.assertEqual(res2, s_res)

        self.assertEqual(self._t_user, res.where(lambda u: u.address.nr == self._t_user.address.nr).single())

    def test_order_by_descending(self):
        res = self._tests.order_by_descending(lambda user: user.address.street).to_list()
        res2 = self._tests.order_by_descending(lambda user: user.address.nr).to_list()
        s_res = self._tests.to_list()
        s_res.sort(key=lambda user: user.address.street, reverse=True)

        self.assertEqual(res, s_res)
        s_res = self._tests.to_list()
        s_res.sort(key=lambda user: user.address.nr, reverse=True)
        self.assertEqual(res2, s_res)

    def test_then_by(self):
        res = self._tests.order_by(lambda user: user.address.street).then_by(lambda user: user.address.nr).to_list()

        s_res = self._tests.to_list()
        s_res.sort(key=lambda user: (user.address.street, user.address.nr))

        self.assertEqual(res, s_res)

    def test_then_by_descending(self):
        res = self._tests.order_by_descending(lambda user: user.address.street).then_by_descending(lambda user: user.address.nr).to_list()

        s_res = self._tests.to_list()
        s_res.sort(key=lambda user: (user.address.street, user.address.nr), reverse=True)

        self.assertEqual(res, s_res)

    def test_reverse(self):
        res = self._tests.reverse()
        l_res = self._tests.to_list()
        l_res.reverse()

        self.assertEqual(res.to_list(), l_res)

    def test_select(self):
        range_list = List(int, range(0, 100))
        selected_range = range_list.select(lambda x: x + 1)

        modulo_range = []
        for x in range(0, 100):
            if x % 2 == 0:
                modulo_range.append(x)
        self.assertEqual(selected_range.to_list(), list(range(1, 101)))
        self.assertEqual(range_list.where(lambda x: x % 2 == 0).to_list(), modulo_range)

    def test_select_many(self):
        range_list = List(int, list(range(0, 100)))
        selected_range = range_list.select(lambda x: [x, x])

        self.assertEqual(selected_range.to_list(), [[x, x] for x in range(0, 100)])
        self.assertEqual(selected_range.select_many(lambda x: x).to_list(), [_x for _l in [2 * [x] for x in range(0, 100)] for _x in _l])

        class TestClass:
            def __init__(self, i, is_sub=False):
                self.i = i
                if is_sub:
                    return
                self.elements = [TestClass(x, True) for x in range(0, 10)]

        elements = List(TestClass, [TestClass(i) for i in range(0, 100)])
        selected_elements = elements.select_many(lambda x: x.elements).select(lambda x: x.i)
        self.assertEqual(selected_elements.where(lambda x: x == 0).count(), 100)

    def test_single(self):
        res = self._tests.where(lambda u: u.address.nr == self._t_user.address.nr)
        s_res = self._tests.where(lambda u: u.address.nr == self._t_user.address.nr).single()

        self.assertEqual(len(res), 1)
        self.assertEqual(self._t_user, s_res)

    def test_single_or_default(self):
        res = self._tests.where(lambda u: u.address.nr == self._t_user.address.nr)
        s_res = self._tests.where(lambda u: u.address.nr == self._t_user.address.nr).single_or_default()
        sn_res = self._tests.where(lambda u: u.address.nr == self._t_user.address.nr + 1).single_or_default()

        self.assertEqual(len(res), 1)
        self.assertEqual(self._t_user, s_res)
        self.assertIsNone(sn_res)

    def test_skip(self):
        skipped = self._tests.skip(5).to_list()

        self.assertEqual(len(skipped), len(self._tests) - 5)
        self.assertEqual(skipped, self._tests[5:])

    def test_skip_last(self):
        skipped = self._tests.skip_last(5)

        self.assertEqual(skipped.count(), len(self._tests) - 5)
        self.assertEqual(skipped.to_list(), self._tests[:-5])
        self.assertEqual(skipped.last(), self._tests[:-5][len(self._tests[:-5]) - 1])

    def test_sum(self):
        res = self._tests.sum(lambda u: u.address.nr)

        s_res = 0
        for user in self._tests:
            s_res += user.address.nr

        self.assertEqual(s_res, res)

        tests = List(values=list(range(0, 100)))
        self.assertEqual(0, tests.min())

        def invalid():
            tests2 = List(str, ['hello', 'world'])
            e_res = tests2.average()

        self.assertRaises(InvalidTypeException, invalid)

    def test_take(self):
        skipped = self._tests.take(5)

        self.assertEqual(skipped.count(), 5)
        self.assertEqual(skipped.to_list(), self._tests[:5])

    def test_take_last(self):
        skipped = self._tests.take_last(5)

        self.assertEqual(skipped.count(), 5)
        self.assertEqual(skipped.to_list(), self._tests[-5:])
        self.assertEqual(skipped.last(), self._tests[len(self._tests) - 1])

    def test_where(self):
        results = []
        for user in self._tests:
            if user.address.nr == 5:
                results.append(user)

        res = self._tests.where(lambda u: u.address.nr == 5)
        self.assertEqual(len(results), len(res))

        def ex():
            e_res = self._tests.where(None)

        self.assertRaises(ArgumentNoneException, ex)
