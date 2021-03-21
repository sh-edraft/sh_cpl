from abc import ABC, abstractmethod

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class StartupABC(ABC):

    @abstractmethod
    def __init__(self, *args):
        """
        ABC for a startup class
        """

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
