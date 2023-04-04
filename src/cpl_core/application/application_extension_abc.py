from abc import ABC, abstractmethod

from cpl_core.configuration import ConfigurationABC
from cpl_core.dependency_injection import ServiceProviderABC


class ApplicationExtensionABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def run(self, config: ConfigurationABC, services: ServiceProviderABC):
        pass

    @abstractmethod
    async def run(self, config: ConfigurationABC, services: ServiceProviderABC):
        pass
