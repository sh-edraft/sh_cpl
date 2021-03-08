from abc import ABC, abstractmethod

from cpl.application.application_host_abc import ApplicationHostABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class StartupABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def create_application_host(self) -> ApplicationHostABC: pass

    @abstractmethod
    def create_configuration(self) -> ConfigurationABC: pass

    @abstractmethod
    def create_services(self) -> ServiceProviderABC: pass
