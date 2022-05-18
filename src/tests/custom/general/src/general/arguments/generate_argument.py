from cpl_core.configuration import ConfigurationABC
from cpl_core.configuration.argument_executable_abc import ArgumentExecutableABC
from cpl_core.console import Console
from cpl_core.environment import ApplicationEnvironmentABC


class GenerateArgument(ArgumentExecutableABC):

    def __init__(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        ArgumentExecutableABC.__init__(self)
        self._config = config
        self._env = env

    def run(self, args: list[str]):
        Console.error('Generate:')
        Console.write_line(args, self._env.environment_name)
