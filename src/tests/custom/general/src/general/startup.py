from cpl_core.application.startup_abc import StartupABC
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.environment import ApplicationEnvironmentABC
from cpl_core.logging.logger_service import Logger
from cpl_core.logging.logger_abc import LoggerABC
from cpl_core.mailing.email_client_service import EMailClient
from cpl_core.mailing.email_client_abc import EMailClientABC
from test_service import TestService


class Startup(StartupABC):

    def __init__(self):
        StartupABC.__init__(self)

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC) -> ConfigurationABC:
        config.add_environment_variables('PYTHON_')
        config.add_environment_variables('CPL_')
        config.add_json_file(f'appsettings.json')
        config.add_json_file(f'appsettings.{config.environment.environment_name}.json')
        config.add_json_file(f'appsettings.{config.environment.host_name}.json', optional=True)

        return config

    def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC) -> ServiceProviderABC:
        services.add_singleton(LoggerABC, Logger)
        services.add_singleton(EMailClientABC, EMailClient)
        services.add_singleton(TestService)

        return services.build_service_provider()
