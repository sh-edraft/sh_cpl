import os
import subprocess

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.workspace_settings import WorkspaceSettings


class CustomScriptService(CommandABC):

    def __init__(self, config: ConfigurationABC, ws: WorkspaceSettings):
        """
        Service for CLI scripts
        """
        CommandABC.__init__(self)

        self._config = config
        self._workspace = ws

    @property
    def help_message(self) -> str:
        return ''

    def execute(self, args: list[str]):
        cmd = self._config.get_configuration('ACTIVE_EXECUTABLE')

        for script in self._workspace.scripts:
            if script != cmd:
                continue

            command = self._workspace.scripts[script]
            try:
                subprocess.run(command, shell=True if os.name == 'posix' else None)
            except Exception as e:
                Console.error(str(e))
