import os
from typing import Optional

from cpl_core.application.startup_abc import StartupABC
from cpl_core.configuration.console_argument import ConsoleArgument
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_cli.command.add_service import AddService
from cpl_cli.command.build_service import BuildService
from cpl_cli.command.custom_script_service import CustomScriptService
from cpl_cli.command.generate_service import GenerateService
from cpl_cli.command.install_service import InstallService
from cpl_cli.command.new_service import NewService
from cpl_cli.command.publish_service import PublishService
from cpl_cli.command.remove_service import RemoveService
from cpl_cli.command.start_service import StartService
from cpl_cli.command.uninstall_service import UninstallService
from cpl_cli.command.update_service import UpdateService
from cpl_cli.command_handler_service import CommandHandler
from cpl_cli.command.help_service import HelpService
from cpl_cli.command.version_service import VersionService
from cpl_cli.configuration.workspace_settings import WorkspaceSettings
from cpl_cli.error import Error
from cpl_cli.live_server.live_server_service import LiveServerService
from cpl_cli.publish.publisher_service import PublisherService
from cpl_cli.publish.publisher_abc import PublisherABC
from cpl_core.environment import ApplicationEnvironment


class Startup(StartupABC):

    def __init__(self):
        StartupABC.__init__(self)

    def configure_configuration(self, configuration: ConfigurationABC, environment: ApplicationEnvironment) -> ConfigurationABC:
        environment.set_runtime_directory(os.path.dirname(__file__))
        configuration.argument_error_function = Error.error

        configuration.add_environment_variables('PYTHON_')
        configuration.add_environment_variables('CPL_')
        configuration.add_json_file('appsettings.json', path=environment.runtime_directory, optional=False, output=False)

        configuration.add_console_argument(ConsoleArgument('', 'add', ['a', 'a'], ' '))
        configuration.add_console_argument(ConsoleArgument('', 'build', ['b', 'B'], ''))
        configuration.add_console_argument(ConsoleArgument('', 'generate', ['g', 'G'], '', console_arguments=[
            ConsoleArgument('', 'abc', ['a', 'A'], ' '),
            ConsoleArgument('', 'class', ['c', 'C'], ' '),
            ConsoleArgument('', 'enum', ['e', 'E'], ' '),
            ConsoleArgument('', 'service', ['s', 'S'], ' '),
            ConsoleArgument('', 'settings', ['st', 'ST'], ' '),
            ConsoleArgument('', 'thread', ['t', 't'], ' ')
        ]))
        configuration.add_console_argument(
            ConsoleArgument('', 'help', ['h', 'H'], ' ', is_value_token_optional=True)
        )
        configuration.add_console_argument(
            ConsoleArgument('', 'install', ['i', 'I'], ' ', is_value_token_optional=True, console_arguments= [
                ConsoleArgument('', '--virtual', ['--v', '--V'], ''),
                ConsoleArgument('', '--simulate', ['--s', '--S'], ''),
            ])
        )
        configuration.add_console_argument(ConsoleArgument('', 'new', ['n', 'N'], '', console_arguments=[
            ConsoleArgument('', 'console', ['c', 'C'], ' '),
            ConsoleArgument('', 'library', ['l', 'L'], ' ')
        ]))
        configuration.add_console_argument(ConsoleArgument('', 'publish', ['p', 'P'], ''))
        configuration.add_console_argument(ConsoleArgument('', 'remove', ['r', 'R'], ' '))
        configuration.add_console_argument(ConsoleArgument('', 'start', ['s', 'S'], ''))
        configuration.add_console_argument(ConsoleArgument('', 'uninstall', ['ui', 'UI'], ' '))
        configuration.add_console_argument(ConsoleArgument('', 'update', ['u', 'U'], ''))
        configuration.add_console_argument(ConsoleArgument('', 'version', ['v', 'V'], ''))

        configuration.add_console_argument(ConsoleArgument('', '--help', ['-h', '-H'], ''))

        if os.path.isfile(os.path.join(environment.working_directory, 'cpl-workspace.json')):
            configuration.add_json_file('cpl-workspace.json', optional=True, output=False)
            workspace: Optional[WorkspaceSettings] = configuration.get_configuration(WorkspaceSettings)
            for script in workspace.scripts:
                configuration.add_console_argument(
                    ConsoleArgument('', script, [], ' ', is_value_token_optional=True))

        configuration.add_console_arguments(error=False)

        return configuration

    def configure_services(self, services: ServiceCollectionABC, environment: ApplicationEnvironment) -> ServiceProviderABC:
        services.add_singleton(CommandHandler)

        services.add_transient(PublisherABC, PublisherService)
        services.add_transient(LiveServerService)

        services.add_transient(AddService)
        services.add_transient(BuildService)
        services.add_transient(CustomScriptService)
        services.add_transient(GenerateService)
        services.add_transient(HelpService)
        services.add_transient(InstallService)
        services.add_transient(NewService)
        services.add_transient(PublishService)
        services.add_transient(RemoveService)
        services.add_transient(StartService)
        services.add_transient(UninstallService)
        services.add_transient(UpdateService)
        services.add_transient(VersionService)

        return services.build_service_provider()
