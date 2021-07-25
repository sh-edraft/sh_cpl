import string
import unittest
from random import randint

from cpl.utils import String
from cpl_query.extension.list import List
from cpl_query.tests.models import User, Address


class QueryTest(unittest.TestCase):

    def setUp(self) -> None:
        self._tests = List()
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
                String.random_string(string.ascii_letters, 8),
                Address(
                    String.random_string(string.ascii_letters, 10),
                    randint(0, 10)
                )
            )

            self._tests.append(user)

        self._tests.append(self._t_user)

    def test_any(self):
        results = []
        for user in self._tests:
            if user.address.nr == 10:
                results.append(user)

        res = self._tests.any(f'User.address.nr == 10')
        n_res = self._tests.any(f'User.address.nr == 100')

        self.assertTrue(res)
        self.assertFalse(n_res)

    def test_first(self):
        results = []
        for user in self._tests:
            if user.address.nr == 10:
                results.append(user)

        res = self._tests.where(f'User.address.nr == 10')
        s_res = self._tests.where(f'User.address.nr == 10').first()

        self.assertEqual(len(res), len(results))
        self.assertIsNotNone(s_res)

    def test_first_or_default(self):
        results = []
        for user in self._tests:
            if user.address.nr == 10:
                results.append(user)

        res = self._tests.where(f'User.address.nr == 10')
        s_res = self._tests.where(f'User.address.nr == 10').first_or_default()
        sn_res = self._tests.where(f'User.address.nr == 11').first_or_default()

        self.assertEqual(len(res), len(results))
        self.assertIsNotNone(s_res)
        self.assertIsNone(sn_res)

    def test_for_each(self):
        users = []
        self._tests.for_each(
            lambda user: (
                # Console.write_line(f'User: {user.name} | '),
                # Console.write(f'Address: {user.address.street}'),
                users.append(user)
            )
        )

        self.assertEqual(len(users), len(self._tests))

    def test_single(self):
        res = self._tests.where(f'User.address.nr == {self._t_user.address.nr}')
        s_res = self._tests.where(f'User.address.nr == {self._t_user.address.nr}').single()

        self.assertEqual(len(res), 1)
        self.assertEqual(self._t_user, s_res)

    def test_single_or_default(self):
        res = self._tests.where(f'User.address.nr == {self._t_user.address.nr}')
        s_res = self._tests.where(f'User.address.nr == {self._t_user.address.nr}').single_or_default()
        sn_res = self._tests.where(f'User.address.nr == {self._t_user.address.nr + 1}').single_or_default()

        self.assertEqual(len(res), 1)
        self.assertEqual(self._t_user, s_res)
        self.assertIsNone(sn_res)

    def test_where(self):
        results = []
        for user in self._tests:
            if user.address.nr == 5:
                results.append(user)

        res = self._tests.where('User.address.nr == 5')
        self.assertEqual(len(results), len(res))
