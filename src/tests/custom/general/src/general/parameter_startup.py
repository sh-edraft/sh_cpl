from cpl_core.application import StartupExtensionABC
from cpl_core.configuration import ConfigurationABC, ArgumentTypeEnum
from cpl_core.dependency_injection import ServiceCollectionABC
from cpl_core.environment import ApplicationEnvironmentABC
from arguments.generate_argument import GenerateArgument
from arguments.install_argument import InstallArgument


class ParameterStartup(StartupExtensionABC):

    def __init__(self):
        StartupExtensionABC.__init__(self)

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'generate', ['g', 'G'], GenerateArgument) \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'abc', ['a', 'A'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'class', ['c', 'C'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'enum', ['e', 'E'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'service', ['s', 'S'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'settings', ['st', 'ST'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'thread', ['t', 'T'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '-', 'o', ['o', 'O'], '=') \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'virtual', ['v', 'V'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'install', ['i', 'I'], InstallArgument) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'virtual', ['v', 'V']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])

    def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC):
        services \
            .add_transient(GenerateArgument) \
            .add_singleton(InstallArgument)
