import os

from cpl_cli.command.add_service import AddService
from cpl_cli.command.build_service import BuildService
from cpl_cli.command.custom_script_service import CustomScriptService
from cpl_cli.command.generate_service import GenerateService
from cpl_cli.command.help_service import HelpService
from cpl_cli.command.install_service import InstallService
from cpl_cli.command.new_service import NewService
from cpl_cli.command.publish_service import PublishService
from cpl_cli.command.remove_service import RemoveService
from cpl_cli.command.start_service import StartService
from cpl_cli.command.uninstall_service import UninstallService
from cpl_cli.command.update_service import UpdateService
from cpl_cli.command.version_service import VersionService
from cpl_cli.error import Error
from cpl_cli.live_server.live_server_service import LiveServerService
from cpl_cli.publish.publisher_abc import PublisherABC
from cpl_cli.publish.publisher_service import PublisherService
from cpl_core.application.startup_abc import StartupABC
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.environment import ApplicationEnvironment


class Startup(StartupABC):

    def __init__(self):
        StartupABC.__init__(self)

    def configure_configuration(self, configuration: ConfigurationABC, environment: ApplicationEnvironment) -> ConfigurationABC:
        environment.set_runtime_directory(os.path.dirname(__file__))
        configuration.argument_error_function = Error.error

        configuration.add_environment_variables('PYTHON_')
        configuration.add_environment_variables('CPL_')
        configuration.add_json_file('appsettings.json', path=environment.runtime_directory, optional=False, output=False)

        return configuration

    def configure_services(self, services: ServiceCollectionABC, environment: ApplicationEnvironment) -> ServiceProviderABC:
        services.add_transient(PublisherABC, PublisherService)
        services.add_transient(LiveServerService)

        services.add_transient(AddService)
        services.add_transient(BuildService)
        services.add_transient(CustomScriptService)
        services.add_transient(GenerateService)
        services.add_transient(HelpService)
        services.add_transient(InstallService)
        services.add_transient(NewService)
        services.add_transient(PublishService)
        services.add_transient(RemoveService)
        services.add_transient(StartService)
        services.add_transient(UninstallService)
        services.add_transient(UpdateService)
        services.add_transient(VersionService)

        return services.build_service_provider()
