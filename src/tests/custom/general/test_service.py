from cpl.console.console import Console
from cpl.dependency_injection import ServiceABC, ServiceProviderABC


class TestService(ServiceABC):

    def __init__(self, provider: ServiceProviderABC):
        ServiceABC.__init__(self)

        self._provider = provider

    def run(self):
        Console.write_line('Hello World!', self._provider)
