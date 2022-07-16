from abc import abstractmethod

from cpl_core.application import ApplicationABC
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC


class DiscordBotApplicationABC(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

    @abstractmethod
    def stop_async(self): pass
