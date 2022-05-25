import os

from cpl_cli.error import Error
from cpl_cli.live_server.live_server_service import LiveServerService
from cpl_cli.publish.publisher_abc import PublisherABC
from cpl_cli.publish.publisher_service import PublisherService
from cpl_core.application.startup_abc import StartupABC
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC


class Startup(StartupABC):

    def __init__(self):
        StartupABC.__init__(self)

    def configure_configuration(self, configuration: ConfigurationABC, environment: ApplicationEnvironmentABC) -> ConfigurationABC:
        environment.set_runtime_directory(os.path.dirname(__file__))
        configuration.argument_error_function = Error.error

        configuration.add_environment_variables('PYTHON_')
        configuration.add_environment_variables('CPL_')
        configuration.add_json_file('appsettings.json', path=environment.runtime_directory, optional=False, output=False)

        return configuration

    def configure_services(self, services: ServiceCollectionABC, environment: ApplicationEnvironmentABC) -> ServiceProviderABC:
        services.add_transient(PublisherABC, PublisherService)
        services.add_transient(LiveServerService)

        return services.build_service_provider()
