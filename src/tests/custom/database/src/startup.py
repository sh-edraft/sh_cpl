from cpl.application import StartupABC
from cpl.configuration import ConfigurationABC
from cpl.database import DatabaseSettings
from cpl.dependency_injection import ServiceProviderABC, ServiceCollectionABC
from cpl.logging import LoggerABC, Logger
from model.db_context import DBContext
from model.user_repo import UserRepo
from model.user_repo_abc import UserRepoABC


class Startup(StartupABC):

    def __init__(self, config: ConfigurationABC, services: ServiceCollectionABC):
        StartupABC.__init__(self)

        self._configuration = config
        self._environment = self._configuration.environment
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
        self._services.add_db_context(DBContext, db_settings)

        self._services.add_singleton(UserRepoABC, UserRepo)

        self._services.add_singleton(LoggerABC, Logger)
        return self._services.build_service_provider()

