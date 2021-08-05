from abc import ABC, abstractmethod
from typing import Optional

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.environment import ApplicationEnvironmentABC


class ApplicationABC(ABC):
    r"""ABC for the Application class

    Parameters
    ----------
        config: :class:`cpl.configuration.configuration_abc.ConfigurationABC`
            Contains object loaded from appsettings
        services: :class:`cpl.dependency_injection.service_provider_abc.ServiceProviderABC`
            Contains instances of prepared objects
    """

    @abstractmethod
    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        self._configuration: Optional[ConfigurationABC] = config
        self._environment: Optional[ApplicationEnvironmentABC] = self._configuration.environment
        self._services: Optional[ServiceProviderABC] = services

    def run(self):
        r"""Entry point

        Called by custom Application.main
        """
        try:
            self.configure()
            self.main()
        except KeyboardInterrupt:
            Console.close()

    @abstractmethod
    def configure(self):
        r"""Configure the application

        Called by :class:`cpl.application.application_abc.ApplicationABC.run`
        """
        pass

    @abstractmethod
    def main(self):
        r"""Custom entry point

        Called by :class:`cpl.application.application_abc.ApplicationABC.run`
        """
        pass
