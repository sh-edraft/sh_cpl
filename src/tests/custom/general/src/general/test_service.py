from abc import ABC

from cpl.console.console import Console
from cpl.dependency_injection import ServiceProviderABC


class TestService(ABC):

    def __init__(self, provider: ServiceProviderABC):
        ABC.__init__(self)

        self._provider = provider

    def run(self):
        Console.write_line('Hello World!', self._provider)
