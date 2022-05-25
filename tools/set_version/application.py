import traceback

from cpl_cli.configuration import WorkspaceSettings
from cpl_core.application import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from set_version.git_service import GitService
from set_version.version_setter_service import VersionSetterService


class Application(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

        self._workspace: WorkspaceSettings = config.get_configuration(WorkspaceSettings)

        self._git_service: GitService = self._services.get_service(GitService)
        self._version_setter: VersionSetterService = self._services.get_service(VersionSetterService)

    def configure(self):
        self._configuration.parse_console_arguments(self._services)

    def main(self):
        Console.write_line('Set versions:')
        args = self._configuration.additional_arguments
        version = {}
        branch = ""
        suffix = ""
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
            version['Major'] = branch.split('.')[0]
            version['Minor'] = branch.split('.')[1]
            version['Micro'] = f'{branch.split(".")[2]}{suffix}'
        except Exception as e:
            Console.error(f'Branch {branch} does not contain valid version')
            return

        try:
            for project in self._workspace.projects:
                if not project.startswith('cpl'):
                    continue

                Console.write_line(f'Set version {version["Major"]}.{version["Minor"]}.{version["Micro"]} for {project}')
                self._version_setter.set_version(self._workspace.projects[project], version)
        except Exception as e:
            Console.error('Version could not be set', traceback.format_exc())
            return
