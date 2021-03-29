from cpl.application import StartupABC
from cpl.configuration import ConfigurationABC
from cpl.dependency_injection import ServiceProviderABC


class Startup(StartupABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        StartupABC.__init__(self)

        self._configuration = config
        self._environment = self._configuration.environment
        self._services = services

    def configure_configuration(self) -> ConfigurationABC:
        return self._configuration

    def configure_services(self) -> ServiceProviderABC:
        return self._services

