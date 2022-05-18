from typing import Type, Optional

from cpl_core.configuration.argument_executable_abc import ArgumentExecutableABC
from cpl_core.configuration.argument_abc import ArgumentABC


class ExecutableArgument(ArgumentABC):

    def __init__(self,
                 token: str,
                 name: str,
                 aliases: list[str],
                 executable: Type[ArgumentExecutableABC],
                 console_arguments: list['ArgumentABC'] = None
                 ):

        self._executable_type = executable
        self._executable: Optional[ArgumentExecutableABC] = None

        ArgumentABC.__init__(self, token, name, aliases, console_arguments)

    @property
    def executable_type(self) -> type:
        return self._executable_type

    def set_executable(self, executable: ArgumentExecutableABC):
        self._executable = executable

    def run(self, args: list[str]):
        r"""Executes runnable if exists
        """
        if self._executable is None:
            return
        self._executable.run(args)
