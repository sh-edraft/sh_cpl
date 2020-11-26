import sys
from datetime import datetime

from sh_edraft.configuration.configuration import Configuration
from sh_edraft.configuration.base.configuration_base import ConfigurationBase
from sh_edraft.hosting.base.environment_base import EnvironmentBase
from sh_edraft.hosting.hosting_environment import HostingEnvironment
from sh_edraft.hosting.application_runtime import ApplicationRuntime
from sh_edraft.hosting.base.application_host_base import ApplicationHostBase
from sh_edraft.service.service_provider import ServiceProvider
from sh_edraft.service.base.service_provider_base import ServiceProviderBase


class ApplicationHost(ApplicationHostBase):

    def __init__(self, name: str):
        ApplicationHostBase.__init__(self)
        self._name: str = name
        self._args: list[str] = sys.argv

        self._config = Configuration()
        self._environment = HostingEnvironment()
        self._app_runtime = ApplicationRuntime(self._config, self._environment)
        self._services = ServiceProvider(self._app_runtime)

        self._start_time: datetime = datetime.now()
        self._end_time: datetime = datetime.now()

    @property
    def name(self) -> str:
        return self._name

    @property
    def environment(self) -> EnvironmentBase:
        return self._environment

    @property
    def configuration(self) -> ConfigurationBase:
        return self._config

    @property
    def services(self) -> ServiceProviderBase:
        return self._services

    def create(self): pass
