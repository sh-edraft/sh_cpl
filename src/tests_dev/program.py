from typing import Optional

from sh_edraft.configuration.base import ConfigurationBase
from sh_edraft.database.connection import DatabaseConnection
from sh_edraft.database.connection.base import DatabaseConnectionBase
from sh_edraft.database.model import DatabaseSettings
from sh_edraft.hosting import ApplicationHost
from sh_edraft.hosting.base import ApplicationBase
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.service.providing.base import ServiceProviderBase
from sh_edraft.utils.credential_manager import CredentialManager


class Program(ApplicationBase):

    def __init__(self):
        ApplicationBase.__init__(self)

        self._app_host: Optional[ApplicationHost] = None
        self._services: Optional[ServiceProviderBase] = None
        self._configuration: Optional[ConfigurationBase] = None
        self._logger: Optional[LoggerBase] = None

    def create_application_host(self):
        self._app_host = ApplicationHost()
        self._configuration = self._app_host.configuration
        self._services = self._app_host.services

    def create_configuration(self):
        self._configuration.add_environment_variables('PYTHON_')
        self._configuration.add_environment_variables('CPL_')
        self._configuration.add_argument_variables()
        self._configuration.add_json_file(f'appsettings.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.environment_name}.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.host_name}.json', optional=True)

    def create_services(self):
        # Create and connect to database
        db_settings: DatabaseSettings = self._configuration.get_configuration(DatabaseSettings)
        self._services.add_singleton(DatabaseConnectionBase, DatabaseConnection)
        db: DatabaseConnectionBase = self._services.get_service(DatabaseConnectionBase)
        db.use_mysql(CredentialManager.build_string(db_settings.connection_string, db_settings.credentials))

        # Add and create logger
        self._services.add_singleton(LoggerBase, Logger)
        self._logger = self._services.get_service(LoggerBase)

    def main(self):
        self._logger.header(f'{self._configuration.environment.application_name}:')
        self._logger.debug(__name__, f'Host: {self._configuration.environment.host_name}')
        self._logger.debug(__name__, f'Environment: {self._configuration.environment.environment_name}')
        self._logger.debug(__name__, f'Customer: {self._configuration.environment.customer}')
