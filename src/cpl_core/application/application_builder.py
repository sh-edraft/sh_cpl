from typing import Type, Optional, Callable, Union

from cpl_core.application.application_abc import ApplicationABC
from cpl_core.application.application_builder_abc import ApplicationBuilderABC
from cpl_core.application.application_extension_abc import ApplicationExtensionABC
from cpl_core.application.startup_abc import StartupABC
from cpl_core.application.startup_extension_abc import StartupExtensionABC
from cpl_core.configuration.configuration import Configuration
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

        self._app_extensions: list[Callable] = []
        self._startup_extensions: list[Callable] = []

    def use_startup(self, startup: Type[StartupABC]):
        self._startup = startup()

    def use_extension(self, extension: Type[Union[ApplicationExtensionABC, StartupExtensionABC]]):
        if issubclass(extension, ApplicationExtensionABC) and extension not in self._app_extensions:
            self._app_extensions.append(extension)
        elif issubclass(extension, StartupExtensionABC) and extension not in self._startup_extensions:
            self._startup_extensions.append(extension)

    def _build_startup(self):
        for ex in self._startup_extensions:
            extension = ex()
            extension.configure_configuration(self._configuration, self._environment)
            extension.configure_services(self._services, self._environment)

        if self._startup is not None:
            self._startup.configure_configuration(self._configuration, self._environment)
            self._startup.configure_services(self._services, self._environment)

    def build(self) -> ApplicationABC:
        self._build_startup()

        config = self._configuration
        services = self._services.build_service_provider()
        config.resolve_runnable_argument_types(services)
        config.parse_console_arguments(error=False)

        for ex in self._app_extensions:
            extension = ex()
            extension.run(config, services)

        return self._app(config, services)

    async def build_async(self) -> ApplicationABC:
        self._build_startup()

        config = self._configuration
        services = self._services.build_service_provider()

        for ex in self._app_extensions:
            extension = ex()
            await extension.run(config, services)

        return self._app(config, services)
