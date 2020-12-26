import base64
import unittest

from sh_edraft.utils import CredentialManager


class CredentialManagerTest(unittest.TestCase):

    def setUp(self): pass

    def test_encode(self):
        test_string = 'Hello World'
        expected_test_result = base64.b64encode(test_string.encode('utf-8')).decode('utf-8')

        test_result = CredentialManager.encrypt(test_string)

        self.assertIsNotNone(test_result)
        self.assertEqual(expected_test_result, test_result)

    def test_decode(self):
        test_string = 'SGVsbG8gV29ybGQ='
        expected_test_result = base64.b64decode(test_string).decode('utf-8')

        test_result = CredentialManager.decrypt(test_string)

        self.assertIsNotNone(test_result)
        self.assertEqual(expected_test_result, test_result)

    def test_build_string(self):
        test_string = 'String is $credentials'
        test_credentials = 'SGVsbG8gV29ybGQ='
        expected_test_result = test_string.replace('$credentials', base64.b64decode(test_credentials).decode('utf-8'))

        test_result = CredentialManager.build_string(test_string, test_credentials)

        self.assertIsNotNone(test_result)
        self.assertEqual(expected_test_result, test_result)
