import os
import sys
import textwrap

from cpl_cli import Error
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration import WorkspaceSettings
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.live_server.start_executable import StartExecutable
from cpl_cli.publish import PublisherService
from cpl_core.configuration import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC


class RunService(CommandABC):

    def __init__(self,
                 config: ConfigurationABC,
                 env: ApplicationEnvironmentABC,
                 services: ServiceProviderABC,
                 project_settings: ProjectSettings,
                 build_settings: BuildSettings,
                 workspace: WorkspaceSettings,
                 publisher: PublisherService,
                 ):
        """
        Service for the CLI command start
        :param config:
        :param env:
        :param services:
        :param project_settings:
        :param build_settings:
        :param workspace:
        """
        CommandABC.__init__(self)

        self._config = config
        self._env = env
        self._services = services
        self._project_settings = project_settings
        self._build_settings = build_settings
        self._workspace = workspace
        self._publisher = publisher

        self._src_dir = os.path.join(self._env.working_directory, self._build_settings.source_path)
        self._is_dev = False

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Starts your application.
        Usage: cpl run
        """)

    def _set_project_by_args(self, name: str):
        if self._workspace is None:
            Error.error('The command requires to be run in an CPL workspace, but a workspace could not be found.')
            sys.exit()

        if name not in self._workspace.projects:
            Error.error(f'Project {name} not found in workspace')
            sys.exit()

        project_path = self._workspace.projects[name]

        self._config.add_configuration(ProjectSettings, None)
        self._config.add_configuration(BuildSettings, None)

        working_directory = self._config.get_configuration('PATH_WORKSPACE')
        if working_directory is not None:
            self._env.set_working_directory(working_directory)

        json_file = os.path.join(self._env.working_directory, project_path)
        self._config.add_json_file(json_file, optional=True, output=False)
        self._project_settings: ProjectSettings = self._config.get_configuration(ProjectSettings)
        self._build_settings: BuildSettings = self._config.get_configuration(BuildSettings)

        if self._project_settings is None or self._build_settings is None:
            Error.error(f'Project {name} not found')
            sys.exit()

        self._src_dir = os.path.dirname(json_file)

    def _build(self):
        if self._is_dev:
            return
        self._publisher.build()

    def execute(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if 'dev' in args:
            self._is_dev = True
            args.remove('dev')

        if len(args) >= 1:
            self._set_project_by_args(args[0])
            args.remove(args[0])

        self._build()

        start_service = StartExecutable(self._env, self._build_settings)
        start_service.run(args, self._project_settings.python_executable, self._src_dir, output=False)
        Console.write_line()
