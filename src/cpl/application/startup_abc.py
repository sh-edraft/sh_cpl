from abc import ABC, abstractmethod

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class StartupABC(ABC):
    r"""ABC for the startup class"""

    @abstractmethod
    def __init__(self, *args):
        pass

    @abstractmethod
    def configure_configuration(self) -> ConfigurationABC:
        r"""Creates configuration of application

        Returns
        -------
            Object of :class:`cpl.configuration.configuration_abc.ConfigurationABC`
        """
        pass

    @abstractmethod
    def configure_services(self) -> ServiceProviderABC:
        r"""Creates service provider

        Returns
        -------
            Object of :class:`cpl.dependency_injection.service_provider_abc.ServiceProviderABC`
        """
        pass
