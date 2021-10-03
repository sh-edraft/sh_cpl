from abc import ABC, abstractmethod

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC


class StartupABC(ABC):
    r"""ABC for the startup class"""

    @abstractmethod
    def __init__(self, *args):
        pass

    @abstractmethod
    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC) -> ConfigurationABC:
        r"""Creates configuration of application

        Parameter
        ---------
            config: :class:`cpl_core.configuration.configuration_abc.ConfigurationABC`
            env: :class:`cpl_core.environment.application_environment_abc`

        Returns
        -------
            Object of :class:`cpl_core.configuration.configuration_abc.ConfigurationABC`
        """
        pass

    @abstractmethod
    def configure_services(self, service: ServiceCollectionABC, env: ApplicationEnvironmentABC) -> ServiceProviderABC:
        r"""Creates service provider

        Parameter
        ---------
            services: :class:`cpl_core.dependency_injection.service_collection_abc`
            env: :class:`cpl_core.environment.application_environment_abc`

        Returns
        -------
            Object of :class:`cpl_core.dependency_injection.service_provider_abc.ServiceProviderABC`
        """
        pass
