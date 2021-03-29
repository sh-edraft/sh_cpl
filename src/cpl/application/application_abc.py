from abc import ABC, abstractmethod
from typing import Optional

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.console import Console
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl.environment import ApplicationEnvironmentABC


class ApplicationABC(ABC):

    @abstractmethod
    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        """
        ABC of application
        """
        self._configuration: Optional[ConfigurationABC] = config
        self._environment: Optional[ApplicationEnvironmentABC] = self._configuration.environment
        self._services: Optional[ServiceProviderABC] = services

    def run(self):
        """
        Entry point
        :return:
        """
        try:
            self.configure()
            self.main()
        except KeyboardInterrupt:
            Console.close()

    @abstractmethod
    def configure(self):
        """
        Prepare the application
        :return:
        """
        pass

    @abstractmethod
    def main(self):
        """
        Custom entry point
        :return:
        """
        pass
