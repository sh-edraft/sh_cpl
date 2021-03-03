from abc import ABC, abstractmethod

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_base import ServiceProviderABC


class ApplicationHostABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def configuration(self) -> ConfigurationABC: pass

    @property
    @abstractmethod
    def application_runtime(self) -> ApplicationRuntimeABC: pass

    @property
    @abstractmethod
    def services(self) -> ServiceProviderABC: pass
