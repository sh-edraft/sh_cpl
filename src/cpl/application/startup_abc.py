from abc import ABC, abstractmethod

from cpl.application.application_host_abc import ApplicationHostABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class StartupABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC for a startup class
        """
        pass

    @abstractmethod
    def create_application_host(self) -> ApplicationHostABC:
        """
        Creates application host with specific attributes
        :return: application host
        """
        pass

    @abstractmethod
    def create_configuration(self) -> ConfigurationABC:
        """
        Creates configuration of application
        :return: configuration
        """
        pass

    @abstractmethod
    def create_services(self) -> ServiceProviderABC:
        """
        Creates service provider
        :return: service provider
        """
        pass
