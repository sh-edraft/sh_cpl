import ssl
from smtplib import SMTP
from typing import Optional

from sh_edraft.environment.base.environment_base import EnvironmentBase
from sh_edraft.logging.base.logger_base import LoggerBase
from sh_edraft.mailing.base.email_client_base import EMailClientBase
from sh_edraft.mailing.model.email import EMail
from sh_edraft.mailing.model.email_client_settings import EMailClientSettings
from sh_edraft.service.base.service_base import ServiceBase
from sh_edraft.utils.credential_manager import CredentialManager


class EMailClient(EMailClientBase):

    def __init__(self, environment: EnvironmentBase, logger: LoggerBase, mail_settings: EMailClientSettings):
        ServiceBase.__init__(self)

        self._environment = environment
        self._mail_settings = mail_settings
        self._logger = logger

        self._server: Optional[SMTP] = None

        self.create()

    def create(self):
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
