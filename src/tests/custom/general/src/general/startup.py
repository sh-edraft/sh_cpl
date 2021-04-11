from cpl.application.startup_abc import StartupABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl.logging.logger_service import Logger
from cpl.logging.logger_abc import LoggerABC
from cpl.mailing.email_client_service import EMailClient
from cpl.mailing.email_client_abc import EMailClientABC
from test_service import TestService


class Startup(StartupABC):

    def __init__(self, config: ConfigurationABC, services: ServiceCollectionABC):
        StartupABC.__init__(self)

        self._configuration = config
        self._services = services

    def configure_configuration(self) -> ConfigurationABC:
        self._configuration.add_environment_variables('PYTHON_')
        self._configuration.add_environment_variables('CPL_')
        self._configuration.add_json_file(f'appsettings.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.environment_name}.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.host_name}.json', optional=True)

        return self._configuration

    def configure_services(self) -> ServiceProviderABC:
        self._services.add_singleton(LoggerABC, Logger)
        self._services.add_singleton(EMailClientABC, EMailClient)
        self._services.add_singleton(TestService)

        return self._services.build_service_provider()
