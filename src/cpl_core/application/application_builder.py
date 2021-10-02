import types
from typing import Type, Optional, Callable

from cpl_core.application.application_abc import ApplicationABC
from cpl_core.application.application_builder_abc import ApplicationBuilderABC
from cpl_core.application.application_extension_abc import ApplicationExtensionABC
from cpl_core.application.startup_abc import StartupABC
from cpl_core.configuration.configuration import Configuration
from cpl_core.console import Console
from cpl_core.dependency_injection.service_collection import ServiceCollection


class ApplicationBuilder(ApplicationBuilderABC):
    r"""This is class is used to build a object of :class:`cpl_core.application.application_abc.ApplicationABC`

    Parameter
    ---------
        app: Type[:class:`cpl_core.application.application_abc.ApplicationABC`]
            Application to build
    """

    def __init__(self, app: Type[ApplicationABC]):
        ApplicationBuilderABC.__init__(self)
        self._app = app
        self._startup: Optional[StartupABC] = None

        self._configuration = Configuration()
        self._environment = self._configuration.environment
        self._services = ServiceCollection(self._configuration)

        self._extensions: list[Callable] = []

    def use_startup(self, startup: Type[StartupABC]):
        self._startup = startup()

    def use_extension(self, extension: Type[ApplicationExtensionABC]):
        if extension not in self._extensions:
            self._extensions.append(extension)

    def build(self) -> ApplicationABC:
        if self._startup is not None:
            self._startup.configure_configuration(self._configuration, self._environment)
            self._startup.configure_services(self._services, self._environment)

        config = self._configuration
        services = self._services.build_service_provider()

        for ex in self._extensions:
            extension = ex()
            extension.run(config, services)

        return self._app(config, services)
