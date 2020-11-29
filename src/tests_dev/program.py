from typing import Optional

from sh_edraft.configuration.base import ConfigurationBase
from sh_edraft.database import DatabaseConnection
from sh_edraft.database.base import DatabaseConnectionBase
from sh_edraft.hosting import ApplicationHost
from sh_edraft.hosting.base import ApplicationBase
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.service.providing.base import ServiceProviderBase


class Program(ApplicationBase):

    def __init__(self):
        ApplicationBase.__init__(self)

        self._app_host: Optional[ApplicationHost] = None
        self._services: Optional[ServiceProviderBase] = None
        self._configuration: Optional[ConfigurationBase] = None
        self._logger: Optional[LoggerBase] = None
        self._db_connection: Optional[DatabaseConnectionBase] = None

    def create_application_host(self):
        self._app_host = ApplicationHost()
        self._configuration = self._app_host.configuration
        self._services = self._app_host.services

    def create_configuration(self):
        self._configuration.create()
        self._configuration.add_environment_variables('PYTHON_')
        self._configuration.add_environment_variables('CPL_')
        self._configuration.add_argument_variables()
        self._configuration.add_json_file(f'appsettings.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.environment_name}.json')
        self._configuration.add_json_file(
            f'appsettings.{self._configuration.environment.host_name}.json',
            optional=True
        )

    def create_services(self):
        self._services.create()
        self._services.add_singleton(LoggerBase, Logger)
        self._services.add_singleton(DatabaseConnectionBase, DatabaseConnection)
        self._logger: Logger = self._services.get_service(LoggerBase)
        self._logger.create()
        self._db_connection: DatabaseConnection = self._services.get_service(DatabaseConnectionBase)
        self._db_connection.create()

    def main(self):
        self._logger.header(f'{self._configuration.environment.application_name}:')
        self._logger.debug(__name__, f'Host: {self._configuration.environment.host_name}')
        self._logger.debug(__name__, f'Environment: {self._configuration.environment.environment_name}')
        self._logger.debug(__name__, f'Customer: {self._configuration.environment.customer}')
