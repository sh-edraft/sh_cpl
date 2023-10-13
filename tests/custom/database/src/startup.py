from cpl_core.application import StartupABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.database import DatabaseSettings
from cpl_core.dependency_injection import ServiceCollectionABC, ServiceProviderABC
from cpl_core.environment import ApplicationEnvironmentABC
from cpl_core.logging import Logger, LoggerABC

from model.db_context import DBContext
from model.user_repo import UserRepo
from model.user_repo_abc import UserRepoABC


class Startup(StartupABC):
    def __init__(self):
        StartupABC.__init__(self)

        self._configuration = None

    def configure_configuration(
        self, configuration: ConfigurationABC, environment: ApplicationEnvironmentABC
    ) -> ConfigurationABC:
        configuration.add_environment_variables("PYTHON_")
        configuration.add_environment_variables("CPL_")
        configuration.add_json_file(f"appsettings.json")
        configuration.add_json_file(f"appsettings.{configuration.environment.environment_name}.json")
        configuration.add_json_file(f"appsettings.{configuration.environment.host_name}.json", optional=True)

        self._configuration = configuration

        return configuration

    def configure_services(
        self, services: ServiceCollectionABC, environment: ApplicationEnvironmentABC
    ) -> ServiceProviderABC:
        # Create and connect to database
        self._configuration.parse_console_arguments(services)
        db_settings: DatabaseSettings = self._configuration.get_configuration(DatabaseSettings)
        services.add_db_context(DBContext, db_settings)

        services.add_singleton(UserRepoABC, UserRepo)

        services.add_singleton(LoggerABC, Logger)
        return services.build_service_provider()
