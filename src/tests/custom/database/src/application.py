from typing import Optional

from cpl_core.application import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from cpl_core.logging import LoggerABC
from model.user_repo_abc import UserRepoABC
from model.user_repo import UserRepo


class Application(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

        self._logger: Optional[LoggerABC] = None

    def configure(self):
        self._logger = self._services.get_service(LoggerABC)

    def main(self):
        self._logger.header(f'{self._configuration.environment.application_name}:')
        self._logger.debug(__name__, f'Host: {self._configuration.environment.host_name}')
        self._logger.debug(__name__, f'Environment: {self._configuration.environment.environment_name}')
        self._logger.debug(__name__, f'Customer: {self._configuration.environment.customer}')

        user_repo: UserRepo = self._services.get_service(UserRepoABC)
        user_repo.add_test_user()
        Console.write_line('Users:')
        for user in user_repo.get_users():
            Console.write_line(user.Id, user.Name, user.City_Id, user.City.Id, user.City.Name, user.City.ZIP)

        Console.write_line('Cities:')
        for city in user_repo.get_cities():
            Console.write_line(city.Id, city.Name, city.ZIP)
