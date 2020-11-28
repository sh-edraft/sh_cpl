from typing import Optional

from sh_edraft.configuration.base import ConfigurationBase
from sh_edraft.hosting import ApplicationHost
from sh_edraft.hosting.base import ApplicationBase
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.service.base import ServiceProviderBase


class Program(ApplicationBase):

    def __init__(self):
        ApplicationBase.__init__(self)

        self._app_host: Optional[ApplicationHost] = None

        self._services: Optional[ServiceProviderBase] = None
        self._configuration: Optional[ConfigurationBase] = None

    def create_application_host(self):
        self._app_host = ApplicationHost()
        self._services = self._app_host.services
        self._configuration = self._app_host.configuration

    def create_configuration(self):
        self._configuration.create()
        self._configuration.add_environment_variables('PYTHON_')
        self._configuration.add_environment_variables('CPL_')
        self._configuration.add_argument_variables()
        self._configuration.add_json_file(f'appsettings.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.environment_name}.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.host_name}.json', optional=True)

    def create_services(self):
        self._services.create()
        self._services.add_singleton(LoggerBase, Logger)
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()
        logger.header(f'{self._configuration.environment.application_name}:')
        logger.debug(__name__, f'Host: {self._configuration.environment.host_name}')
        logger.debug(__name__, f'Environment: {self._configuration.environment.environment_name}')
        logger.debug(__name__, f'Customer: {self._configuration.environment.customer}')

    def main(self):
        print('RUN')
