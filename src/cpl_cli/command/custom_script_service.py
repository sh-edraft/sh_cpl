import os
import subprocess

from cpl_core.environment import ApplicationEnvironmentABC

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.workspace_settings import WorkspaceSettings


class CustomScriptService(CommandABC):

    def __init__(self, config: ConfigurationABC, env: ApplicationEnvironmentABC, ws: WorkspaceSettings):
        """
        Service for CLI scripts
        """
        CommandABC.__init__(self)

        self._config = config
        self._env = env
        self._workspace = ws

    @property
    def help_message(self) -> str:
        return ''

    def execute(self, args: list[str]):
        cmd = self._config.get_configuration('ACTIVE_EXECUTABLE')
        wd = self._config.get_configuration('PATH_WORKSPACE')
        if wd is not None:
            self._env.set_working_directory(wd)

        for script in self._workspace.scripts:
            if script != cmd:
                continue

            command = self._workspace.scripts[script]
            try:
                subprocess.run(command, shell=True if os.name == 'posix' else None)
            except Exception as e:
                Console.error(str(e))
