from typing import Type, Optional

from cpl.application.application_abc import ApplicationABC
from cpl.application.application_builder_abc import ApplicationBuilderABC
from cpl.application.startup_abc import StartupABC
from cpl.configuration.configuration import Configuration
from cpl.dependency_injection.service_collection import ServiceCollection


class ApplicationBuilder(ApplicationBuilderABC):
    r"""This is class is used to build a object of :class:`cpl.application.application_abc.ApplicationABC`

    Parameter
    ---------
        app: Type[:class:`cpl.application.application_abc.ApplicationABC`]
            Application to build
    """

    def __init__(self, app: Type[ApplicationABC]):
        ApplicationBuilderABC.__init__(self)
        self._app = app
        self._startup: Optional[StartupABC] = None

        self._configuration = Configuration()
        self._environment = self._configuration.environment
        self._services = ServiceCollection(self._configuration)

    def use_startup(self, startup: Type[StartupABC]):
        self._startup = startup(self._configuration, self._services)

    def build(self) -> ApplicationABC:
        if self._startup is not None:
            self._startup.configure_configuration()
            self._startup.configure_services()

        return self._app(self._configuration, self._services.build_service_provider())
