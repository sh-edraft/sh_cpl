import os

from cpl.application.startup_abc import StartupABC
from cpl.configuration.console_argument import ConsoleArgument
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_cli.command.build_service import BuildService
from cpl_cli.command.generate_service import GenerateService
from cpl_cli.command.install_service import InstallService
from cpl_cli.command.new_service import NewService
from cpl_cli.command.publish_service import PublishService
from cpl_cli.command.start_service import StartService
from cpl_cli.command.uninstall_service import UninstallService
from cpl_cli.command.update_service import UpdateService
from cpl_cli.command_handler_service import CommandHandler
from cpl_cli.command.help_service import HelpService
from cpl_cli.command.version_service import VersionService
from cpl_cli.error import Error
from cpl_cli.live_server.live_server_service import LiveServerService
from cpl_cli.publish.publisher_service import PublisherService
from cpl_cli.publish.publisher_abc import PublisherABC


class Startup(StartupABC):

    def __init__(self, config: ConfigurationABC, services: ServiceCollectionABC):
        StartupABC.__init__(self)

        self._configuration = config
        self._env = self._configuration.environment
        self._services = services

        self._env.set_runtime_directory(os.path.dirname(__file__))

    def configure_configuration(self) -> ConfigurationABC:
        self._configuration.argument_error_function = Error.error

        self._configuration.add_environment_variables('PYTHON_')
        self._configuration.add_environment_variables('CPL_')
        self._configuration.add_json_file('appsettings.json', path=self._env.runtime_directory,
                                          optional=False, output=False)
        self._configuration.add_console_argument(
            ConsoleArgument('', 'build', ['b', 'B'], ' ', is_value_token_optional=True)
        )
        self._configuration.add_console_argument(ConsoleArgument('', 'generate', ['g', 'G'], '', console_arguments=[
            ConsoleArgument('', 'abc', ['a', 'A'], ' '),
            ConsoleArgument('', 'class', ['c', 'C'], ' '),
            ConsoleArgument('', 'enum', ['e', 'E'], ' '),
            ConsoleArgument('', 'service', ['s', 'S'], ' '),
            ConsoleArgument('', 'settings', ['st', 'ST'], ' '),
            ConsoleArgument('', 'thread', ['t', 't'], ' ')
        ]))
        self._configuration.add_console_argument(ConsoleArgument('', 'help', ['h', 'H'], ''))
        self._configuration.add_console_argument(
            ConsoleArgument('', 'install', ['i', 'I'], ' ', is_value_token_optional=True)
        )
        self._configuration.add_console_argument(ConsoleArgument('', 'new', ['n', 'N'], '', console_arguments=[
            ConsoleArgument('', 'console', ['c', 'C'], ' '),
            ConsoleArgument('', 'library', ['l', 'L'], ' ')
        ]))
        self._configuration.add_console_argument(ConsoleArgument('', 'publish', ['p', 'P'], ''))
        self._configuration.add_console_argument(
            ConsoleArgument('', 'start', ['s', 'S'], ' ', is_value_token_optional=True)
        )
        self._configuration.add_console_argument(ConsoleArgument('', 'uninstall', ['ui', 'UI'], ' '))
        self._configuration.add_console_argument(ConsoleArgument('', 'update', ['u', 'U'], ''))
        self._configuration.add_console_argument(ConsoleArgument('', 'version', ['v', 'V'], ''))
        self._configuration.add_console_arguments(error=False)

        return self._configuration

    def configure_services(self) -> ServiceProviderABC:
        self._services.add_singleton(CommandHandler)

        self._services.add_transient(PublisherABC, PublisherService)
        self._services.add_transient(LiveServerService)

        self._services.add_transient(BuildService)
        self._services.add_transient(GenerateService)
        self._services.add_transient(HelpService)
        self._services.add_transient(InstallService)
        self._services.add_transient(NewService)
        self._services.add_transient(PublishService)
        self._services.add_transient(StartService)
        self._services.add_transient(UninstallService)
        self._services.add_transient(UpdateService)
        self._services.add_transient(VersionService)

        return self._services.build_service_provider()
