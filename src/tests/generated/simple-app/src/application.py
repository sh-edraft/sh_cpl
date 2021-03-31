from cpl.application import ApplicationABC
from cpl.configuration import ConfigurationABC
from cpl.console import Console
from cpl.dependency_injection import ServiceProviderABC


class Application(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

    def configure(self):
        pass

    def main(self):
        Console.write_line('Hello World')
