from abc import ABC, abstractmethod
from typing import Type, Optional

from cpl.application.application_host_abc import ApplicationHostABC
from cpl.application.startup_abc import StartupABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_base import ServiceProviderABC


class ApplicationABC(ABC):

    @abstractmethod
    def __init__(self):
        self._startup: Optional[StartupABC] = None
        self._app_host: Optional[ApplicationHostABC] = None
        self._services: Optional[ServiceProviderABC] = None
        self._configuration: Optional[ConfigurationABC] = None

    def use_startup(self, startup: Type[StartupABC]):
        self._startup = startup()

    def build(self):
        if self._startup is None:
            print('Startup is empty')
            exit()

        self._app_host = self._startup.create_application_host()
        self._configuration = self._startup.create_configuration()
        self._services = self._startup.create_services()

    @abstractmethod
    def run(self): pass
