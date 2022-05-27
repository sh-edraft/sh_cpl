import os
import traceback

from cpl_core.utils import String

from cpl_cli.configuration.version_settings_name_enum import VersionSettingsNameEnum
from cpl_cli.configuration.workspace_settings import WorkspaceSettings
from cpl_core.application.application_abc import ApplicationABC
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.pipes.version_pipe import VersionPipe
from set_version.git_service import GitService
from set_version.version_setter_service import VersionSetterService


class Application(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

        self._workspace: WorkspaceSettings = config.get_configuration(WorkspaceSettings)

        self._git_service: GitService = self._services.get_service(GitService)
        self._version_setter: VersionSetterService = self._services.get_service(VersionSetterService)
        self._version_pipe: VersionPipe = self._services.get_service(VersionPipe)

    def configure(self):
        self._configuration.parse_console_arguments(self._services)

    def main(self):
        Console.write_line('Set versions:')

        args = self._configuration.additional_arguments
        version = {}
        branch = ""
        suffix = ""
        force = False
        if '--force' in args:
            args.remove('--force')
            force = True

        if len(args) > 1:
            Console.error(f'Unexpected argument(s): {", ".join(args[1:])}')
            return

        if len(args) == 1:
            suffix = f'.{args[0]}'

        try:
            branch = self._git_service.get_active_branch_name()
            Console.write_line(f'Found branch: {branch}')
        except Exception as e:
            Console.error('Branch could not be found', traceback.format_exc())
            return

        try:
            version[VersionSettingsNameEnum.major.value] = branch.split('.')[0]
            version[VersionSettingsNameEnum.minor.value] = branch.split('.')[1]
            version[VersionSettingsNameEnum.micro.value] = f'{branch.split(".")[2]}{suffix}'
        except Exception as e:
            Console.error(f'Branch {branch} does not contain valid version')
            return

        diff_paths = []
        for file in self._git_service.get_diff_files():
            if '/' in file:
                diff_paths.append(file.split('/')[1])
            else:
                diff_paths.append(os.path.basename(os.path.dirname(file)))

        try:
            skipped = []
            for project in self._workspace.projects:
                if project not in diff_paths and String.convert_to_snake_case(project) not in diff_paths and not force:
                    Console.write_line(f'Skipping {project} due to missing changes')
                    skipped.append(project)
                    continue

                Console.write_line(f'Set dependencies {self._version_pipe.transform(version)} for {project}')
                self._version_setter.set_dependencies(self._workspace.projects[project], version, skipped=skipped)
                if not project.startswith('cpl') and not project.startswith('unittest'):
                    Console.write_line(f'Skipping {project}')
                    continue

                Console.write_line(f'Set version {self._version_pipe.transform(version)} for {project}')
                self._version_setter.set_version(self._workspace.projects[project], version)
        except Exception as e:
            Console.error('Version could not be set', traceback.format_exc())
            return
