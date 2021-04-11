from collections import Callable

from cpl_cli.command_abc import CommandABC


class CommandModel:

    def __init__(self, name: str, aliases: list[str], command: Callable[CommandABC], is_workspace_needed: bool,
                 is_project_needed: bool, change_cwd: bool):
        self._name = name
        self._aliases = aliases
        self._command = command
        self._is_workspace_needed = is_workspace_needed
        self._is_project_needed = is_project_needed
        self._change_cwd = change_cwd

    @property
    def name(self) -> str:
        return self._name

    @property
    def aliases(self) -> list[str]:
        return self._aliases

    @property
    def command(self) -> Callable[CommandABC]:
        return self._command
    
    @property
    def is_workspace_needed(self) -> bool:
        return self._is_workspace_needed

    @property
    def is_project_needed(self) -> bool:
        return self._is_project_needed

    @property
    def change_cwd(self) -> bool:
        return self._change_cwd
