from cpl_core.application import ApplicationExtensionABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceProviderABC


class TestExtension(ApplicationExtensionABC):

    def __init__(self):
        ApplicationExtensionABC.__init__(self)

    def run(self, config: ConfigurationABC, services: ServiceProviderABC):
        Console.write_line('Hello World from App Extension')
