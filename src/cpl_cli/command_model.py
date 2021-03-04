from collections import Callable

from cpl_cli.command_abc import CommandABC


class CommandModel:

    def __init__(self, name: str, aliases: list[str], command: Callable[CommandABC]):
        self._name = name
        self._aliases = aliases
        self._command = command

    @property
    def name(self) -> str:
        return self._name

    @property
    def aliases(self) -> list[str]:
        return self._aliases
    
    @property
    def command(self) -> Callable[CommandABC]:
        return self._command
