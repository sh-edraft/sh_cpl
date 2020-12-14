from datetime import datetime

from sh_edraft.configuration.configuration import Configuration
from sh_edraft.configuration.base.configuration_base import ConfigurationBase
from sh_edraft.hosting.base.application_runtime_base import ApplicationRuntimeBase
from sh_edraft.hosting.application_runtime import ApplicationRuntime
from sh_edraft.hosting.base.application_host_base import ApplicationHostBase
from sh_edraft.service.providing.service_provider import ServiceProvider
from sh_edraft.service.providing.base.service_provider_base import ServiceProviderBase


class ApplicationHost(ApplicationHostBase):

    def __init__(self):
        ApplicationHostBase.__init__(self)

        # Init
        self._config = Configuration()
        self._app_runtime = ApplicationRuntime(self._config)
        self._services = ServiceProvider(self._app_runtime)

        # Create
        self._config.create()
        self._services.create()

        # Set vars
        self._start_time: datetime = datetime.now()
        self._end_time: datetime = datetime.now()

    @property
    def configuration(self) -> ConfigurationBase:
        return self._config

    @property
    def application_runtime(self) -> ApplicationRuntimeBase:
        return self._app_runtime

    @property
    def services(self) -> ServiceProviderBase:
        return self._services

    def create(self): pass
