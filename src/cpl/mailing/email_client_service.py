import ssl
from smtplib import SMTP
from typing import Optional

from cpl.environment.environment_abc import EnvironmentABC
from cpl.logging.logger_abc import LoggerABC
from cpl.mailing.email import EMail
from cpl.mailing.email_client_abc import EMailClientABC
from cpl.mailing.email_client_settings import EMailClientSettings
from cpl.utils.credential_manager import CredentialManager


class EMailClient(EMailClientABC):

    def __init__(self, environment: EnvironmentABC, logger: LoggerABC, mail_settings: EMailClientSettings):
        """
        Service to send emails
        :param environment:
        :param logger:
        :param mail_settings:
        """
        EMailClientABC.__init__(self)

        self._environment = environment
        self._mail_settings = mail_settings
        self._logger = logger

        self._server: Optional[SMTP] = None

        self.create()

    def create(self):
        """
        Creates connection
        :return:
        """
        self._logger.trace(__name__, f'Started {__name__}.create')
        self.connect()
        self._logger.trace(__name__, f'Stopped {__name__}.create')

    def connect(self):
        """
        Connects to server
        :return:
        """
        self._logger.trace(__name__, f'Started {__name__}.connect')
        try:
            self._logger.debug(__name__, f'Try to connect to {self._mail_settings.host}:{self._mail_settings.port}')
            self._server = SMTP(self._mail_settings.host, self._mail_settings.port)
            self._logger.info(__name__, f'Connected to {self._mail_settings.host}:{self._mail_settings.port}')

            self._logger.debug(__name__, 'Try to start tls')
            self._server.starttls(context=ssl.create_default_context())
            self._logger.info(__name__, 'Started tls')
        except Exception as e:
            self._logger.error(__name__, 'Cannot connect to mail server', e)

        self._logger.trace(__name__, f'Stopped {__name__}.connect')

    def login(self):
        """
        Login to server
        :return:
        """
        self._logger.trace(__name__, f'Started {__name__}.login')
        try:
            self._logger.debug(__name__, f'Try to login {self._mail_settings.user_name}@{self._mail_settings.host}:{self._mail_settings.port}')
            self._server.login(self._mail_settings.user_name, CredentialManager.decrypt(self._mail_settings.credentials))
            self._logger.info(__name__, f'Logged on as {self._mail_settings.user_name} to {self._mail_settings.host}:{self._mail_settings.port}')
        except Exception as e:
            self._logger.error(__name__, 'Cannot login to mail server', e)

        self._logger.trace(__name__, f'Stopped {__name__}.login')

    def send_mail(self, email: EMail):
        """
        Sends email
        :param email:
        :return:
        """
        self._logger.trace(__name__, f'Started {__name__}.send_mail')
        try:
            self.login()
            email.body += f'\n\nDies ist eine automatische E-Mail.' \
                          f'\nGesendet von {self._environment.application_name}-{self._environment.environment_name}@{self._environment.host_name} für ' \
                          f'{self._environment.customer}.'

            self._logger.debug(__name__, f'Try to send email to {email.receiver_list}')
            self._server.sendmail(self._mail_settings.user_name, email.receiver_list, email.get_content(self._mail_settings.user_name))
            self._logger.info(__name__, f'Sent email to {email.receiver_list}')
        except Exception as e:
            self._logger.error(__name__, f'Cannot send mail to {email.receiver_list}', e)
        self._logger.trace(__name__, f'Stopped {__name__}.send_mail')
