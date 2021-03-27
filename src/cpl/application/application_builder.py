from typing import Type, Optional

from cpl.application.application_abc import ApplicationABC
from cpl.application.application_builder_abc import ApplicationBuilderABC
from cpl.application.application_runtime import ApplicationRuntime
from cpl.application.startup_abc import StartupABC
from cpl.configuration import Configuration
from cpl.dependency_injection.service_collection import ServiceCollection


class ApplicationBuilder(ApplicationBuilderABC):

    def __init__(self, app: Type[ApplicationABC]):
        """
        Builder class for application
        """
        ApplicationBuilderABC.__init__(self)
        self._app = app
        self._startup: Optional[StartupABC] = None

        self._configuration = Configuration()
        self._runtime = ApplicationRuntime()
        self._services = ServiceCollection(self._configuration, self._runtime)

    def use_startup(self, startup: Type[StartupABC]):
        """
        Sets the used startup class
        :param startup:
        :return:
        """
        self._startup = startup(self._configuration, self._runtime, self._services)

    def build(self) -> ApplicationABC:
        """
        Creates application host and runtime
        :return:
        """
        if self._startup is not None:
            self._startup.configure_configuration()
            self._startup.configure_services()

        return self._app(self._configuration, self._runtime, self._services.build_service_provider())
