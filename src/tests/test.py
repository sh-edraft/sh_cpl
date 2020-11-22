import os
import sys
from typing import Optional

from termcolor import colored

from sh_edraft.service import ServiceProvider
from tests.publisher import PublisherTest
from tests.service_provider import ServiceProviderTest


class Test:

    def __init__(self):
        self._services: Optional[ServiceProvider] = None

        self._tests = [
            ServiceProviderTest,
            PublisherTest
        ]

        self._error: bool = False

    @staticmethod
    def block_print():
        sys.stdout = open(os.devnull, 'w')

    @staticmethod
    def enable_print():
        sys.stdout = sys.__stdout__

    def success(self, message: str):
        self.enable_print()
        print(colored(message, 'green'))
        self.block_print()

    def failed(self, message: str):
        self.enable_print()
        print(colored(message, 'red'))
        self.block_print()

    def create(self): pass

    def start(self):
        self.block_print()

        if not self._error:
            try:
                self._services = ServiceProviderTest.start()
                self.success(f'{ServiceProviderTest.__name__} test succeeded.')
            except Exception as e:
                self._error = True
                self.failed(f'{ServiceProviderTest.__name__} test failed!\n{e}')

        if not self._error:
            try:
                PublisherTest.start(self._services)
                self.success(f'{PublisherTest.__name__} test succeeded.')
            except Exception as e:
                self._error = True
                self.failed(f'{PublisherTest.__name__} test failed!\n{e}')


if __name__ == '__main__':
    test = Test()
    test.create()
    test.start()
