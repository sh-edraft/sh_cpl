import string
import unittest
from random import randint

from cpl.utils import String
from cpl_query.exceptions import InvalidTypeException, WrongTypeException, ArgumentNoneException
from cpl_query.extension.list import List
from cpl_query.tests.models import User, Address


class QueryTest(unittest.TestCase):

    def setUp(self) -> None:
        self._tests = List(User)
        self._t_user = User(
            'Test user',
            Address(
                'teststr.',
                15
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
        res = self._tests.average(int, lambda u: u.address.nr)

        self.assertEqual(res, avg)

        def invalid():
            e_res = self._tests.average(str, lambda u: u.address.nr)

        def wrong():
            e_res = self._tests.average(int, lambda u: u.address.street)

        self.assertRaises(InvalidTypeException, invalid)
        self.assertRaises(WrongTypeException, wrong)

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
        self._tests.for_each(
            lambda user: (
                users.append(user)
            )
        )

        self.assertEqual(len(users), len(self._tests))

    def test_max(self):
        res = self._tests.max(int, lambda u: u.address.nr)
        self.assertEqual(self._t_user.address.nr, res)

    def test_min(self):
        res = self._tests.min(int, lambda u: u.address.nr)
        self.assertEqual(1, res)

    def test_order_by(self):
        res = self._tests.order_by(lambda user: user.address.street)
        res2 = self._tests.order_by(lambda user: user.address.nr)
        s_res = self._tests
        s_res.sort(key=lambda user: user.address.street)

        self.assertEqual(res, s_res)
        s_res.sort(key=lambda user: user.address.nr)
        self.assertEqual(res2, s_res)

    def test_order_by_descending(self):
        res = self._tests.order_by_descending(lambda user: user.address.street)
        res2 = self._tests.order_by_descending(lambda user: user.address.nr)
        s_res = self._tests
        s_res.sort(key=lambda user: user.address.street, reverse=True)

        self.assertEqual(res, s_res)
        s_res.sort(key=lambda user: user.address.nr, reverse=True)
        self.assertEqual(res2, s_res)

    def test_then_by(self):
        res = self._tests.order_by(lambda user: user.address.street[0]).then_by(lambda user: user.address.nr)

        s_res = self._tests
        s_res.sort(key=lambda user: (user.address.street[0], user.address.nr))

        self.assertEqual(res, s_res)

    def test_then_by_descending(self):
        res = self._tests.order_by_descending(lambda user: user.address.street[0]).then_by_descending(
            lambda user: user.address.nr)

        s_res = self._tests
        s_res.sort(key=lambda user: (user.address.street[0], user.address.nr), reverse=True)

        self.assertEqual(res, s_res)

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
