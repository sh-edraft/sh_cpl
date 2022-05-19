import os
from typing import Optional

from cpl_cli.command.add_service import AddService
from cpl_cli.command.build_service import BuildService
from cpl_cli.command.custom_script_service import CustomScriptService
from cpl_cli.command.generate_service import GenerateService
from cpl_cli.command.help_service import HelpService
from cpl_cli.command.install_service import InstallService
from cpl_cli.command.new_service import NewService
from cpl_cli.command.publish_service import PublishService
from cpl_cli.command.remove_service import RemoveService
from cpl_cli.command.start_service import StartService
from cpl_cli.command.uninstall_service import UninstallService
from cpl_cli.command.update_service import UpdateService
from cpl_cli.command.version_service import VersionService
from cpl_cli.configuration.workspace_settings import WorkspaceSettings
from cpl_core.application import StartupExtensionABC
from cpl_core.configuration.argument_type_enum import ArgumentTypeEnum
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.environment import ApplicationEnvironmentABC
from cpl_core.utils import String


class StartupArgumentExtension(StartupExtensionABC):

    def __init__(self):
        pass

    @staticmethod
    def _search_project_json(env: ApplicationEnvironmentABC) -> Optional[str]:
        project_name = None
        name = os.path.basename(env.working_directory)
        for r, d, f in os.walk(env.working_directory):
            for file in f:
                if file.endswith('.json'):
                    f_name = file.split('.json')[0]
                    if f_name == name or \
                            String.convert_to_camel_case(f_name).lower() == String.convert_to_camel_case(
                        name).lower():
                        project_name = f_name
                        break

        return project_name

    def _read_cpl_environment(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        workspace: Optional[WorkspaceSettings] = config.get_configuration(WorkspaceSettings)
        if workspace is not None:
            for script in workspace.scripts:
                config.create_console_argument(ArgumentTypeEnum.Executable, '', script, [], CustomScriptService)

            project = workspace.projects[workspace.default_project]
        else:
            project = f'{self._search_project_json(env)}.json'

        config.add_json_file(project, optional=True, output=False)

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        config.add_json_file('cpl-workspace.json', path=env.working_directory, optional=True, output=False)

        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'add', ['a', 'A'], AddService) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'build', ['b', 'B'], BuildService)
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'generate', ['g', 'G'], GenerateService) \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'abc', ['a', 'A'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'class', ['c', 'C'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'enum', ['e', 'E'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'service', ['s', 'S'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'settings', ['st', 'ST'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'thread', ['t', 't'], ' ')
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'install', ['i', 'I'], InstallService) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'virtual', ['v', 'V']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'new', ['n', 'N'], NewService) \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'console', ['c', 'C'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'library', ['l', 'L'], ' ')
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'publish', ['p', 'P'], PublishService)
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'remove', ['r', 'R'], RemoveService) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'start', ['S', 'S'], StartService)
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'uninstall', ['ui', 'UI'], UninstallService) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'virtual', ['v', 'V']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'update', ['u', 'U'], UpdateService)
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'version', ['v', 'V'], VersionService)

        config.for_each_argument(
            lambda a: a.add_console_argument(ArgumentTypeEnum.Executable, '--', 'help', ['h', 'H'], HelpService)
        )
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'help', ['h', 'H'], HelpService)

        self._read_cpl_environment(config, env)

    def configure_services(self, service: ServiceCollectionABC, env: ApplicationEnvironmentABC):
        pass
