import time
from typing import Optional

from cpl_core.application.application_abc import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from cpl_core.logging import LoggerABC
from cpl_core.mailing import EMailClientABC, EMail
from cpl_core.pipes import IPAddressPipe
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
        self._configuration.parse_console_arguments(self._services)

        if self._configuration.environment.application_name != '':
            self._logger.header(f'{self._configuration.environment.application_name}:')
        self._logger.debug(__name__, f'Args: {self._configuration.additional_arguments}')
        self._logger.debug(__name__, f'Host: {self._configuration.environment.host_name}')
        self._logger.debug(__name__, f'Environment: {self._configuration.environment.environment_name}')
        self._logger.debug(__name__, f'Customer: {self._configuration.environment.customer}')
        Console.spinner('Test', self._wait, 2, spinner_foreground_color='red')
        test: TestService = self._services.get_service(TestService)
        ip_pipe: IPAddressPipe = self._services.get_service(IPAddressPipe)
        test.run()
        test2: TestService = self._services.get_service(TestService)
        ip_pipe2: IPAddressPipe = self._services.get_service(IPAddressPipe)
        Console.write_line(f'DI working: {test == test2 and ip_pipe != ip_pipe2}')
        Console.write_line(self._services.get_service(LoggerABC))
        # self.test_send_mail()
