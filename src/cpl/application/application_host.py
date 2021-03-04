from datetime import datetime

from cpl.application.application_host_abc import ApplicationHostABC
from cpl.application.application_runtime import ApplicationRuntime
from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration import Configuration
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider import ServiceProvider
from cpl.dependency_injection.service_provider_base import ServiceProviderABC


class ApplicationHost(ApplicationHostABC):

    def __init__(self):
        ApplicationHostABC.__init__(self)

        # Init
        self._config = Configuration()
        self._app_runtime = ApplicationRuntime(self._config)
        self._services = ServiceProvider(self._app_runtime)

        # Set vars
        self._start_time: datetime = datetime.now()
        self._end_time: datetime = datetime.now()

    @property
    def configuration(self) -> ConfigurationABC:
        return self._config

    @property
    def application_runtime(self) -> ApplicationRuntimeABC:
        return self._app_runtime

    @property
    def services(self) -> ServiceProviderABC:
        return self._services

    def create(self): pass
