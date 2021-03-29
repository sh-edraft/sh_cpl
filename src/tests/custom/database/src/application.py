from typing import Optional

from cpl.application import ApplicationABC
from cpl.configuration import ConfigurationABC
from cpl.console import Console
from cpl.dependency_injection import ServiceProviderABC
from cpl.logging import LoggerABC


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
