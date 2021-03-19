from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.application.startup_abc import StartupABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.database.context.database_context import DatabaseContext
from cpl.database.database_settings import DatabaseSettings
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl.logging.logger_service import Logger
from cpl.logging.logger_abc import LoggerABC
from cpl.mailing.email_client_service import EMailClient
from cpl.mailing.email_client_abc import EMailClientABC
from cpl.utils.credential_manager import CredentialManager


class Startup(StartupABC):

    def __init__(self, config: ConfigurationABC, runtime: ApplicationRuntimeABC, services: ServiceProviderABC):
        StartupABC.__init__(self)

        self._configuration = config
        self._application_runtime = runtime
        self._services = services

    def configure_configuration(self) -> ConfigurationABC:
        self._configuration.add_environment_variables('PYTHON_')
        self._configuration.add_environment_variables('CPL_')
        self._configuration.add_console_arguments()
        self._configuration.add_json_file(f'appsettings.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.environment_name}.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.host_name}.json', optional=True)

        return self._configuration

    def configure_services(self) -> ServiceProviderABC:
        # Create and connect to database
        db_settings: DatabaseSettings = self._configuration.get_configuration(DatabaseSettings)
        self._services.add_db_context(DatabaseContext)
        db: DatabaseContext = self._services.get_db_context()
        db.connect(CredentialManager.build_string(db_settings.connection_string, db_settings.credentials))

        self._services.add_singleton(LoggerABC, Logger)
        self._services.add_singleton(EMailClientABC, EMailClient)

        return self._services
