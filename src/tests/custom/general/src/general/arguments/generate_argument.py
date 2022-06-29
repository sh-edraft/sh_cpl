from cpl_core.configuration import ConfigurationABC, ArgumentExecutableABC
from cpl_core.console import Console
from cpl_core.environment import ApplicationEnvironmentABC


class GenerateArgument(ArgumentExecutableABC):

    def __init__(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        ArgumentExecutableABC.__init__(self)
        self._config = config
        self._env = env

    def execute(self, args: list[str]):
        Console.error('Generate:')
        Console.write_line(args, self._env.environment_name)
