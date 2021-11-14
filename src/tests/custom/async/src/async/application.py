from cpl_core.application import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceProviderABC


class Application(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

    async def configure(self):
        pass

    async def main(self):
        Console.write_line('Hello World')
