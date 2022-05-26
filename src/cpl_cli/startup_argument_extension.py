import os
from typing import Optional

from cpl_core.console import Console

from cpl_cli.command.add_service import AddService
from cpl_cli.command.build_service import BuildService
from cpl_cli.command.custom_script_service import CustomScriptService
from cpl_cli.command.generate_service import GenerateService
from cpl_cli.command.help_service import HelpService
from cpl_cli.command.install_service import InstallService
from cpl_cli.command.new_service import NewService
from cpl_cli.command.publish_service import PublishService
from cpl_cli.command.remove_service import RemoveService
from cpl_cli.command.run_service import RunService
from cpl_cli.command.start_service import StartService
from cpl_cli.command.uninstall_service import UninstallService
from cpl_cli.command.update_service import UpdateService
from cpl_cli.command.version_service import VersionService
from cpl_cli.configuration.workspace_settings import WorkspaceSettings
from cpl_cli.validators.project_validator import ProjectValidator
from cpl_cli.validators.workspace_validator import WorkspaceValidator
from cpl_core.application.startup_extension_abc import StartupExtensionABC
from cpl_core.configuration.argument_type_enum import ArgumentTypeEnum
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_core.utils.string import String


class StartupArgumentExtension(StartupExtensionABC):

    def __init__(self):
        pass

    @staticmethod
    def _search_project_json(working_directory: str) -> Optional[str]:
        project_name = None
        name = os.path.basename(working_directory)
        for r, d, f in os.walk(working_directory):
            for file in f:
                if file.endswith('.json'):
                    f_name = file.split('.json')[0]
                    if f_name == name or String.convert_to_camel_case(f_name).lower() == String.convert_to_camel_case(name).lower():
                        project_name = f_name
                        break

        return project_name

    def _read_cpl_environment(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        workspace: Optional[WorkspaceSettings] = config.get_configuration(WorkspaceSettings)
        config.add_configuration('PATH_WORKSPACE', env.working_directory)
        if workspace is not None:
            for script in workspace.scripts:
                config.create_console_argument(ArgumentTypeEnum.Executable, '', script, [], CustomScriptService)
            return

        project = self._search_project_json(env.working_directory)
        if project is not None:
            project = f'{project}.json'

        if project is None:
            return

        config.add_json_file(project, optional=True, output=False)

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        config.add_json_file('cpl-workspace.json', path=env.working_directory, optional=True, output=False)

        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'add', ['a', 'A'], AddService, True, validators=[WorkspaceValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'build', ['b', 'B'], BuildService, True, validators=[ProjectValidator])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'generate', ['g', 'G'], GenerateService, True) \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'abc', ['a', 'A'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'class', ['c', 'C'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'enum', ['e', 'E'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'pipe', ['p', 'P'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'service', ['s', 'S'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'settings', ['st', 'ST'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'test_case', ['tc', 'TC'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'thread', ['t', 'T'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'validator', ['v', 'V'], ' ')
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'install', ['i', 'I'], InstallService, True, validators=[ProjectValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'virtual', ['v', 'V']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'new', ['n', 'N'], NewService, True) \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'console', ['c', 'C'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'library', ['l', 'L'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'unittest', ['ut', 'UT'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'async', ['a', 'A']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'application-base', ['ab', 'AB']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'startup', ['s', 'S']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'service-providing', ['sp', 'SP']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'nothing', ['n', 'N'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'publish', ['p', 'P'], PublishService, True, validators=[ProjectValidator])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'remove', ['r', 'R'], RemoveService, True, validators=[WorkspaceValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'run', [], RunService, True, validators=[ProjectValidator])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'start', ['s', 'S'], StartService, True, validators=[ProjectValidator])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'uninstall', ['ui', 'UI'], UninstallService, True, validators=[ProjectValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'virtual', ['v', 'V']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'update', ['u', 'U'], UpdateService, True, validators=[ProjectValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'version', ['v', 'V'], VersionService, True)

        config.for_each_argument(lambda a: a.add_console_argument(ArgumentTypeEnum.Flag, '--', 'help', ['h', 'H']))
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'help', ['h', 'H'], HelpService)

        self._read_cpl_environment(config, env)

    def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC):
        services.add_transient(WorkspaceValidator)
        services.add_transient(ProjectValidator)

        services.add_transient(AddService)
        services.add_transient(BuildService)
        services.add_transient(CustomScriptService)
        services.add_transient(GenerateService)
        services.add_transient(HelpService)
        services.add_transient(InstallService)
        services.add_transient(NewService)
        services.add_transient(PublishService)
        services.add_transient(RemoveService)
        services.add_transient(RunService)
        services.add_transient(StartService)
        services.add_transient(UninstallService)
        services.add_transient(UpdateService)
        services.add_transient(VersionService)
