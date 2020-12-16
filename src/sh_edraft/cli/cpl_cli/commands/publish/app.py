from typing import Optional

from sh_edraft.configuration.base.configuration_base import ConfigurationBase
from sh_edraft.hosting.application_host import ApplicationHost
from sh_edraft.hosting.base.application_base import ApplicationBase
from sh_edraft.logging.logger import Logger
from sh_edraft.logging.base.logger_base import LoggerBase
from sh_edraft.publishing.publisher import Publisher
from sh_edraft.publishing.base.publisher_base import PublisherBase
from sh_edraft.service.providing.base.service_provider_base import ServiceProviderBase


class PublishApp(ApplicationBase):

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
        self._configuration.add_json_file(f'build.json')

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
        self._publisher.create()
        self._publisher.build()
        self._publisher.publish()
