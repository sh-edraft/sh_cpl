from typing import Optional

from sh_edraft.configuration.base import ConfigurationBase
from sh_edraft.console import Console
from sh_edraft.hosting import ApplicationHost
from sh_edraft.hosting.base import ApplicationBase
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.publishing import Publisher
from sh_edraft.publishing.base import PublisherBase
from sh_edraft.service.providing.base import ServiceProviderBase


class Program(ApplicationBase):

    def __init__(self):
        ApplicationBase.__init__(self)

        self._app_host: Optional[ApplicationHost] = None
        self._services: Optional[ServiceProviderBase] = None
        self._configuration: Optional[ConfigurationBase] = None
        self._logger: Optional[LoggerBase] = None
        self._publisher: Optional[PublisherBase] = None

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
        # Add and create logger
        self._services.add_singleton(LoggerBase, Logger)
        self._logger = self._services.get_service(LoggerBase)

        # Add and create publisher
        self._services.add_singleton(PublisherBase, Publisher)
        self._publisher: Publisher = self._services.get_service(PublisherBase)

    def main(self):
        self._logger.header(f'{self._configuration.environment.application_name}:')
        self._logger.debug(__name__, f'Host: {self._configuration.environment.host_name}')
        self._logger.debug(__name__, f'Environment: {self._configuration.environment.environment_name}')
        self._logger.debug(__name__, f'Customer: {self._configuration.environment.customer}')
        self._publisher.exclude('../tests')
        self._publisher.exclude('../tests_dev')
        self._publisher.create()
        self._publisher.publish()


if __name__ == '__main__':
    program = Program()
    program.create_application_host()
    program.create_configuration()
    program.create_services()
    program.main()
