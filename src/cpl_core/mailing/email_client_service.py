import ssl
from smtplib import SMTP
from typing import Optional

from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_core.logging.logger_abc import LoggerABC
from cpl_core.mailing.email import EMail
from cpl_core.mailing.email_client_abc import EMailClientABC
from cpl_core.mailing.email_client_settings import EMailClientSettings
from cpl_core.utils.credential_manager import CredentialManager


class EMailClient(EMailClientABC):
    r"""Service to send emails

    Parameter
    ---------
        environment: :class:`cpl.environment.application_environment_abc.ApplicationEnvironmentABC`
            Environment of the application
        logger: :class:`cpl.logging.logger_abc.LoggerABC`
            The logger to use
        mail_settings: :class:`cpl.mailing.email_client_settings.EMailClientSettings`
            Settings for mailing
    """

    def __init__(self, environment: ApplicationEnvironmentABC, logger: LoggerABC, mail_settings: EMailClientSettings):
        EMailClientABC.__init__(self)

        self._environment = environment
        self._mail_settings = mail_settings
        self._logger = logger

        self._server: Optional[SMTP] = None

        self.create()

    def create(self):
        r"""Creates connection"""
        self._logger.trace(__name__, f'Started {__name__}.create')
        self.connect()
        self._logger.trace(__name__, f'Stopped {__name__}.create')

    def connect(self):
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
        r"""Login to server"""
        self._logger.trace(__name__, f'Started {__name__}.login')
        try:
            self._logger.debug(__name__, f'Try to login {self._mail_settings.user_name}@{self._mail_settings.host}:{self._mail_settings.port}')
            self._server.login(self._mail_settings.user_name, CredentialManager.decrypt(self._mail_settings.credentials))
            self._logger.info(__name__, f'Logged on as {self._mail_settings.user_name} to {self._mail_settings.host}:{self._mail_settings.port}')
        except Exception as e:
            self._logger.error(__name__, 'Cannot login to mail server', e)

        self._logger.trace(__name__, f'Stopped {__name__}.login')

    def send_mail(self, email: EMail):
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
