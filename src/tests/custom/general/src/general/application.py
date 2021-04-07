import time
from typing import Optional

from cpl.application.application_abc import ApplicationABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.console import Console
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl.logging.logger_abc import LoggerABC
from cpl.mailing.email import EMail
from cpl.mailing.email_client_abc import EMailClientABC
from test_service import TestService


class Application(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)
        self._logger: Optional[LoggerABC] = None
        self._mailer: Optional[EMailClientABC] = None

    def test_send_mail(self):
        mail = EMail()
        mail.add_header('Mime-Version: 1.0')
        mail.add_header('Content-Type: text/plain; charset=utf-8')
        mail.add_header('Content-Transfer-Encoding: quoted-printable')
        mail.add_receiver('sven.heidemann@sh-edraft.de')
        mail.subject = f'Test - {self._configuration.environment.host_name}'
        mail.body = 'Dies ist ein Test :D'
        self._mailer.send_mail(mail)

    @staticmethod
    def _wait(time_ms: int):
        time.sleep(time_ms)

    def configure(self):
        self._logger = self._services.get_service(LoggerABC)
        self._mailer = self._services.get_service(EMailClientABC)

    def main(self):
        self._logger.header(f'{self._configuration.environment.application_name}:')
        self._logger.debug(__name__, f'Host: {self._configuration.environment.host_name}')
        self._logger.debug(__name__, f'Environment: {self._configuration.environment.environment_name}')
        self._logger.debug(__name__, f'Customer: {self._configuration.environment.customer}')
        Console.spinner('Test', self._wait, 2, spinner_foreground_color='red')
        test: TestService = self._services.get_service(TestService)
        test.run()
        # self.test_send_mail()
