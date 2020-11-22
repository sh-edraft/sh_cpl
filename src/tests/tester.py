import os
import sys
import traceback
from typing import Optional

from termcolor import colored

from sh_edraft.configuration import ApplicationHost
from sh_edraft.service import ServiceProvider
from tests.logger import LoggerTest
from tests.publisher import PublisherTest
from tests.service_provider import ServiceProviderTest


class Tester:

    def __init__(self):
        self._app_host = ApplicationHost()
        self._services: Optional[ServiceProvider] = None

        self._error: bool = False

    @staticmethod
    def disable_print():
        sys.stdout = open(os.devnull, 'w')

    @staticmethod
    def enable_print():
        sys.stdout = sys.__stdout__

    def success(self, message: str):
        self.enable_print()
        print(colored(message, 'green'))
        self.disable_print()

    def failed(self, message: str):
        self.enable_print()
        print(colored(message, 'red'))
        self.disable_print()

    def exception(self):
        self.enable_print()
        print(colored(traceback.format_exc(), 'red'))
        self.disable_print()

    def create(self): pass

    def start(self):
        self.disable_print()

        if not self._error:
            try:
                ServiceProviderTest.start(self._app_host.services)
                self.success(f'{ServiceProviderTest.__name__} test succeeded.')
            except Exception as e:
                self._error = True
                self.failed(f'{ServiceProviderTest.__name__} test failed!\n{e}')
                self.exception()

        if not self._error:
            try:
                LoggerTest.start(self._app_host)
                self.success(f'{LoggerTest.__name__} test succeeded.')
            except Exception as e:
                self._error = True
                self.failed(f'{LoggerTest.__name__} test failed!\n{e}')
                self.exception()

        if not self._error:
            try:
                PublisherTest.start(self._app_host.services)
                self.success(f'{PublisherTest.__name__} test succeeded.')
            except Exception as e:
                self._error = True
                self.failed(f'{PublisherTest.__name__} test failed!\n{e}')
                self.exception()


if __name__ == '__main__':
    tester = Tester()
    tester.create()
    tester.start()
