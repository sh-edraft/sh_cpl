from abc import ABC, abstractmethod
from typing import Optional

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.console import Console
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class ApplicationABC(ABC):

    @abstractmethod
    def __init__(self, config: ConfigurationABC, runtime: ApplicationRuntimeABC, services: ServiceProviderABC):
        """
        ABC of application
        """
        self._configuration: Optional[ConfigurationABC] = config
        self._runtime: Optional[ApplicationRuntimeABC] = runtime
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
