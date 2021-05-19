import traceback

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.console.console import Console
from cpl.mailing.email_client_settings_name_enum import EMailClientSettingsNameEnum


class EMailClientSettings(ConfigurationModelABC):
    r"""Representation of mailing settings"""

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self._host: str = ''
        self._port: int = 0
        self._user_name: str = ''
        self._credentials: str = ''

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, host: str) -> None:
        self._host = host

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, port: int) -> None:
        self._port = port

    @property
    def user_name(self) -> str:
        return self._user_name

    @user_name.setter
    def user_name(self, user_name: str) -> None:
        self._user_name = user_name

    @property
    def credentials(self) -> str:
        return self._credentials

    @credentials.setter
    def credentials(self, credentials: str) -> None:
        self._credentials = credentials

    def from_dict(self, settings: dict):
        try:
            self._host = settings[EMailClientSettingsNameEnum.host.value]
            self._port = settings[EMailClientSettingsNameEnum.port.value]
            self._user_name = settings[EMailClientSettingsNameEnum.user_name.value]
            self._credentials = settings[EMailClientSettingsNameEnum.credentials.value]
        except Exception as e:
            Console.error(f'[ ERROR ] [ {__name__} ]: Reading error in {self.__name__} settings')
            Console.error(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')

