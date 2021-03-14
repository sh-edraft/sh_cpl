from abc import ABC, abstractmethod
from typing import Type, Optional

from cpl.application.application_host_abc import ApplicationHostABC
from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.application.startup_abc import StartupABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class ApplicationABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC of application
        """
        self._startup: Optional[StartupABC] = None
        self._app_host: Optional[ApplicationHostABC] = None
        self._configuration: Optional[ConfigurationABC] = None
        self._runtime: Optional[ApplicationRuntimeABC] = None
        self._services: Optional[ServiceProviderABC] = None

    def use_startup(self, startup: Type[StartupABC]):
        """
        Sets the used startup class
        :param startup:
        :return:
        """
        self._startup = startup()

    def build(self):
        """
        Creates application host and runtime
        :return:
        """
        if self._startup is not None:
            self._app_host = self._startup.create_application_host()
            self._runtime = self._app_host.application_runtime
            self._configuration = self._startup.create_configuration()
            self._services = self._startup.create_services()

    def run(self):
        """
        Entry point
        :return:
        """
        self.configure()
        self.main()

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
