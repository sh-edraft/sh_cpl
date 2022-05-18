from cpl_core.application import StartupExtensionABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.dependency_injection import ServiceCollectionABC
from cpl_core.environment import ApplicationEnvironmentABC
from arguments.generate_argument import GenerateArgument
from arguments.install_argument import InstallArgument


class ParameterStartup(StartupExtensionABC):

    def __init__(self):
        StartupExtensionABC.__init__(self)

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        config.create_console_argument('', 'generate', ['g', 'G'], '', runnable=GenerateArgument) \
            .add_console_argument('', 'abc', ['a', 'A'], ' ') \
            .add_console_argument('', 'class', ['c', 'C'], ' ') \
            .add_console_argument('', 'enum', ['e', 'E'], ' ') \
            .add_console_argument('', 'service', ['s', 'S'], ' ') \
            .add_console_argument('', 'settings', ['st', 'ST'], ' ') \
            .add_console_argument('', 'thread', ['t', 'T'], ' ') \
            .add_console_argument('-', 'o', ['o', 'O'], '=')
        config.create_console_argument('', 'install', ['i', 'I'], ' ', is_value_token_optional=True,
                                       runnable=InstallArgument) \
            .add_console_argument('--', 'virtual', ['v', 'V'], '') \
            .add_console_argument('--', 'simulate', ['s', 'S'], '')

    def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC):
        services \
            .add_singleton(GenerateArgument) \
            .add_singleton(InstallArgument)
