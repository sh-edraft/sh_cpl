import atexit
from collections import Callable

from cpl.application.application_host_abc import ApplicationHostABC
from cpl.application.application_runtime import ApplicationRuntime
from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration import Configuration
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.console import Console
from cpl.dependency_injection.service_provider import ServiceProvider
from cpl.dependency_injection.service_provider_base import ServiceProviderABC


class ApplicationHost(ApplicationHostABC):

    def __init__(self):
        ApplicationHostABC.__init__(self)

        # Init
        self._config = Configuration()
        self._app_runtime = ApplicationRuntime(self._config)
        self._services = ServiceProvider(self._app_runtime)

    @property
    def configuration(self) -> ConfigurationABC:
        return self._config

    @property
    def application_runtime(self) -> ApplicationRuntimeABC:
        return self._app_runtime

    @property
    def services(self) -> ServiceProviderABC:
        return self._services

    @staticmethod
    def output_at_exit():
        atexit.register(Console.close)

    def console_argument_error_function(self, function: Callable):
        self._config.argument_error_function = function
