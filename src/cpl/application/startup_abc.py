from abc import ABC, abstractmethod

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class StartupABC(ABC):

    @abstractmethod
    def __init__(self, config: ConfigurationABC, runtime: ApplicationRuntimeABC, services: ServiceProviderABC):
        """
        ABC for a startup class
        """

        self._configuration = config
        self._application_runtime = runtime
        self._services = services

    @abstractmethod
    def configure_configuration(self) -> ConfigurationABC:
        """
        Creates configuration of application
        :return: configuration
        """
        pass

    @abstractmethod
    def configure_services(self) -> ServiceProviderABC:
        """
        Creates service provider
        :return: service provider
        """
        pass
