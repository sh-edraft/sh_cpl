from abc import ABC, abstractmethod

from sh_edraft.configuration.base.configuration_base import ConfigurationBase
from sh_edraft.hosting.base.application_runtime_base import ApplicationRuntimeBase
from sh_edraft.hosting.base.environment_base import EnvironmentBase
from sh_edraft.service.base.service_provider_base import ServiceProviderBase


class ApplicationHostBase(ABC):

    @abstractmethod
    def __init__(self): pass
    
    @property
    @abstractmethod
    def name(self) -> str: pass

    @property
    @abstractmethod
    def configuration(self) -> ConfigurationBase: pass

    @property
    @abstractmethod
    def environment(self) -> EnvironmentBase: pass

    @property
    @abstractmethod
    def application_runtime(self) -> ApplicationRuntimeBase: pass

    @property
    @abstractmethod
    def services(self) -> ServiceProviderBase: pass

    @abstractmethod
    def create(self): pass
