from abc import ABC, abstractmethod
from collections import Callable

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class ApplicationHostABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def configuration(self) -> ConfigurationABC: pass

    @property
    @abstractmethod
    def application_runtime(self) -> ApplicationRuntimeABC: pass

    @property
    @abstractmethod
    def services(self) -> ServiceProviderABC: pass

    @staticmethod
    @abstractmethod
    def output_at_exit(): pass

    @abstractmethod
    def console_argument_error_function(self, function: Callable): pass
