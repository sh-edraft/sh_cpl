from cpl_core.application import StartupExtensionABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceCollectionABC
from cpl_core.environment import ApplicationEnvironmentABC


class TestStartupExtension(StartupExtensionABC):

    def __init__(self):
        StartupExtensionABC.__init__(self)

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        Console.write_line('config')

    def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC):
        Console.write_line('services')
