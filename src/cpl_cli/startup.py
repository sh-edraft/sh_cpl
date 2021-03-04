from typing import Optional

from cpl.application.application_host import ApplicationHost
from cpl.application.application_host_abc import ApplicationHostABC
from cpl.application.startup_abc import StartupABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_provider_base import ServiceProviderABC
from cpl_cli.command_handler import CommandHandler
from cpl_cli.commands.help import Help
from cpl_cli.commands.version import Version
from cpl_cli.error import Error


class Startup(StartupABC):

    def __init__(self):
        StartupABC.__init__(self)

        self._app_host: Optional[ApplicationHostABC] = None
        self._configuration: Optional[ConfigurationABC] = None
        self._services: Optional[ServiceProviderABC] = None

    def create_application_host(self) -> ApplicationHostABC:
        self._app_host = ApplicationHost()

        self._app_host.application_runtime.set_runtime_directory(__file__)
        self._app_host.console_argument_error_function(Error.error)

        self._configuration = self._app_host.configuration
        self._services = self._app_host.services

        return self._app_host

    def create_configuration(self) -> ConfigurationABC:
        self._configuration.add_environment_variables('PYTHON_')
        self._configuration.add_environment_variables('CPL_')
        self._configuration.add_console_argument('', 'help', ['-h', '-H'], '')
        self._configuration.add_console_argument('', 'version', ['-v', '-V'], '')
        self._configuration.add_console_arguments()

        return self._configuration

    def create_services(self) -> ServiceProviderABC:
        self._services.add_singleton(CommandHandler, CommandHandler)

        self._services.add_scoped(Help, Help)
        self._services.add_scoped(Version, Version)

        return self._services
