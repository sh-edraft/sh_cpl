import unittest

from tests.cases.utils.credential_manager import CredentialManagerTest


class Tester:

    def __init__(self):
        self._suite = unittest.TestSuite()

    def create(self):
        self._suite.addTest(CredentialManagerTest(CredentialManagerTest.test_encode.__name__))
        self._suite.addTest(CredentialManagerTest(CredentialManagerTest.test_decode.__name__))
        self._suite.addTest(CredentialManagerTest(CredentialManagerTest.test_build_string.__name__))

    def start(self):
        runner = unittest.TextTestRunner()
        runner.run(self._suite)


if __name__ == '__main__':
    tester = Tester()
    tester.create()
    tester.start()
