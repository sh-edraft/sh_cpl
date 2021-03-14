from abc import ABC, abstractmethod
from collections import Callable

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class ApplicationHostABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC for application host
        """
        pass

    @property
    @abstractmethod
    def configuration(self) -> ConfigurationABC: pass

    @property
    @abstractmethod
    def application_runtime(self) -> ApplicationRuntimeABC: pass

    @property
    @abstractmethod
    def services(self) -> ServiceProviderABC: pass

    @abstractmethod
    def console_argument_error_function(self, function: Callable):
        """
        Defines function to call when a argument error is detected
        :param function:
        :return:
        """
        pass
