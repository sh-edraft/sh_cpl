from cpl_core.application import StartupABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.dependency_injection import ServiceProviderABC, ServiceCollectionABC
from cpl_core.environment import ApplicationEnvironment


class Startup(StartupABC):
    def __init__(self):
        StartupABC.__init__(self)

    def configure_configuration(
        self, configuration: ConfigurationABC, environment: ApplicationEnvironment
    ) -> ConfigurationABC:
        configuration.add_json_file("appsettings.json")
        return configuration

    def configure_services(
        self, services: ServiceCollectionABC, environment: ApplicationEnvironment
    ) -> ServiceProviderABC:
        services.add_translation()
        return services.build_service_provider()
