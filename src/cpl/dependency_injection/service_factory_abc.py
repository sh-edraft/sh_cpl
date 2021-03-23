from abc import ABC, abstractmethod

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_descriptor import ServiceDescriptor


class ServiceFactoryABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def service_descriptors(self) -> list[ServiceDescriptor]: pass

    @property
    @abstractmethod
    def configuration(self) -> ConfigurationABC: pass

    @property
    @abstractmethod
    def runtime(self) -> ApplicationRuntimeABC: pass
