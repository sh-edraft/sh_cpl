from cpl_cli.command.add_service import AddService
from cpl_cli.command.build_service import BuildService
from cpl_cli.command.generate_service import GenerateService
from cpl_cli.command.help_service import HelpService
from cpl_cli.command.install_service import InstallService
from cpl_cli.command.new_service import NewService
from cpl_cli.command.publish_service import PublishService
from cpl_cli.command.remove_service import RemoveService
from cpl_cli.command.run_service import RunService
from cpl_cli.command.start_service import StartService
from cpl_cli.command.uninstall_service import UninstallService
from cpl_cli.command.update_service import UpdateService
from cpl_cli.command.version_service import VersionService
from cpl_cli.validators.project_validator import ProjectValidator
from cpl_cli.validators.workspace_validator import WorkspaceValidator
from cpl_core.application.startup_extension_abc import StartupExtensionABC
from cpl_core.configuration.argument_type_enum import ArgumentTypeEnum
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC


class StartupArgumentExtension(StartupExtensionABC):

    def __init__(self):
        pass

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'add', ['a', 'A'], AddService, True, validators=[WorkspaceValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'build', ['b', 'B'], BuildService, True, validators=[ProjectValidator])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'generate', ['g', 'G'], GenerateService, True) \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'abc', ['a', 'A'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'class', ['c', 'C'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'enum', ['e', 'E'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'pipe', ['p', 'P'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'service', ['s', 'S'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'settings', ['st', 'ST'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'test_case', ['tc', 'TC'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'thread', ['t', 'T'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'validator', ['v', 'V'], ' ')
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'install', ['i', 'I'], InstallService, True, validators=[ProjectValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'dev', ['d', 'D']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'virtual', ['v', 'V']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'cpl-prod', ['cp', 'CP']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'cpl-exp', ['ce', 'CE']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'cpl-dev', ['cd', 'CD'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'new', ['n', 'N'], NewService, True) \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'console', ['c', 'C'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'library', ['l', 'L'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Variable, '', 'unittest', ['ut', 'UT'], ' ') \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'async', ['a', 'A']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'application-base', ['ab', 'AB']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'startup', ['s', 'S']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'service-providing', ['sp', 'SP']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'nothing', ['n', 'N']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'venv', ['v', 'V']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'base', ['b', 'B'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'publish', ['p', 'P'], PublishService, True, validators=[ProjectValidator])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'remove', ['r', 'R'], RemoveService, True, validators=[WorkspaceValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'run', [], RunService, True, validators=[ProjectValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'dev', ['d', 'D'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'start', ['s', 'S'], StartService, True, validators=[ProjectValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'dev', ['d', 'D'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'uninstall', ['ui', 'UI'], UninstallService, True, validators=[ProjectValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'dev', ['d', 'D']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'virtual', ['v', 'V']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'update', ['u', 'U'], UpdateService, True, validators=[ProjectValidator]) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'simulate', ['s', 'S']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'cpl-prod', ['cp', 'CP']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'cpl-exp', ['ce', 'CE']) \
            .add_console_argument(ArgumentTypeEnum.Flag, '--', 'cpl-dev', ['cd', 'CD'])
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'version', ['v', 'V'], VersionService, True)

        config.for_each_argument(lambda a: a.add_console_argument(ArgumentTypeEnum.Flag, '--', 'help', ['h', 'H']))
        config.create_console_argument(ArgumentTypeEnum.Executable, '', 'help', ['h', 'H'], HelpService)

    def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC):
        pass
