from cpl_core.application import StartupABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.dependency_injection import ServiceCollectionABC, ServiceProviderABC
from cpl_core.environment import ApplicationEnvironmentABC
from cpl_core.logging import Logger, LoggerABC
from cpl_core.mailing import EMailClient, EMailClientABC
from cpl_core.pipes import IPAddressPipe
from test_service import TestService


class Startup(StartupABC):
    def __init__(self):
        StartupABC.__init__(self)

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC) -> ConfigurationABC:
        config.add_environment_variables("PYTHON_")
        config.add_environment_variables("CPLT_")
        config.add_json_file(f"appsettings.json")
        config.add_json_file(f"appsettings.{config.environment.environment_name}.json")
        config.add_json_file(f"appsettings.{config.environment.host_name}.json", optional=True)

        return config

    def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC) -> ServiceProviderABC:
        services.add_singleton(LoggerABC, Logger)
        services.add_singleton(EMailClientABC, EMailClient)
        services.add_transient(IPAddressPipe)
        services.add_singleton(TestService)

        return services.build_service_provider()
