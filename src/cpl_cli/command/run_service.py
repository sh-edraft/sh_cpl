import os
import textwrap

from cpl_cli.command_abc import CommandABC
from cpl_core.console.console import Console
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.live_server.live_server_thread import LiveServerThread


class RunService(CommandABC):

    def __init__(self, env: ApplicationEnvironmentABC, project_settings: ProjectSettings, build_settings: BuildSettings):
        """
        Service for the CLI command start
        :param env:
        :param project_settings:
        :param build_settings:
        """
        CommandABC.__init__(self)

        self._env = env
        self._project_settings = project_settings
        self._build_settings = build_settings

        self._src_dir = os.path.join(self._env.working_directory, self._build_settings.source_path)

        self._args: list[str] = []

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Starts your application.
        Usage: cpl run
        """)

    def execute(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        ls_thread = LiveServerThread(
            self._project_settings.python_executable,
            self._src_dir,
            self._args,
            self._env,
            self._build_settings
        )
        ls_thread.start()
        ls_thread.join()
        Console.write_line()
