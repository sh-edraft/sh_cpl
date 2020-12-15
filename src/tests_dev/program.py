from typing import Optional

from sh_edraft.configuration.base import ConfigurationBase
from sh_edraft.database.context import DatabaseContext
from sh_edraft.database.model import DatabaseSettings
from sh_edraft.hosting import ApplicationHost
from sh_edraft.hosting.base import ApplicationBase
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.service.providing.base import ServiceProviderBase
from sh_edraft.utils import CredentialManager, Console

from tests_dev.db.user_repo import UserRepo
from tests_dev.db.user_repo_base import UserRepoBase


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
        self._services.add_db_context(DatabaseContext)
        db: DatabaseContext = self._services.get_db_context()
        db.connect(CredentialManager.build_string(db_settings.connection_string, db_settings.credentials))

        self._services.add_scoped(UserRepoBase, UserRepo)

        # Add and create logger
        self._services.add_singleton(LoggerBase, Logger)
        self._logger = self._services.get_service(LoggerBase)

    def main(self):
        self._logger.header(f'{self._configuration.environment.application_name}:')
        self._logger.debug(__name__, f'Host: {self._configuration.environment.host_name}')
        self._logger.debug(__name__, f'Environment: {self._configuration.environment.environment_name}')
        self._logger.debug(__name__, f'Customer: {self._configuration.environment.customer}')
        self._services.get_service(UserRepoBase).add_test_user()

        Console.clear()
        Console.write_line('Hello', 'World')
        # name = Console.read_line('Name: ')
        # Console.write_line('Hello', name)
        Console.set_foreground_color('red')
        Console.set_background_color('green')
        Console.set_cursor_position(5, 5)
        Console.write_line('Error')
        Console.write_line_at(10, 10, 'Error')
        Console.reset_cursor_position()
        Console.set_foreground_color('green')
        Console.set_background_color('default')
        Console.write('Test')
        Console.write_line('1')
        Console.write_line(Console.foreground_color)
