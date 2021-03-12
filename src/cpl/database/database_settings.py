import traceback
from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColor
from cpl.database.database_settings_name_enum import DatabaseSettingsName


class DatabaseSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self._auth_plugin: Optional[str] = None
        self._connection_string: Optional[str] = None
        self._credentials: Optional[str] = None
        self._encoding: Optional[str] = None
        self._case_sensitive: Optional[bool] = None
        self._echo: Optional[bool] = None

    @property
    def auth_plugin(self) -> str:
        return self._auth_plugin

    @auth_plugin.setter
    def auth_plugin(self, auth_plugin: str):
        self._auth_plugin = auth_plugin

    @property
    def connection_string(self) -> str:
        return self._connection_string

    @connection_string.setter
    def connection_string(self, connection_string: str):
        self._connection_string = connection_string

    @property
    def credentials(self) -> str:
        return self._credentials

    @credentials.setter
    def credentials(self, credentials: str):
        self._credentials = credentials

    @property
    def encoding(self) -> str:
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: str) -> None:
        self._encoding = encoding

    @property
    def case_sensitive(self) -> bool:
        return self._case_sensitive

    @case_sensitive.setter
    def case_sensitive(self, case_sensitive: bool) -> None:
        self._case_sensitive = case_sensitive

    @property
    def echo(self) -> bool:
        return self._echo

    @echo.setter
    def echo(self, echo: bool) -> None:
        self._echo = echo

    def from_dict(self, settings: dict):
        try:
            self._connection_string = settings[DatabaseSettingsName.connection_string.value]
            self._credentials = settings[DatabaseSettingsName.credentials.value]

            if DatabaseSettingsName.auth_plugin.value in settings:
                self._auth_plugin = settings[DatabaseSettingsName.auth_plugin.value]

            if DatabaseSettingsName.encoding.value in settings:
                self._encoding = settings[DatabaseSettingsName.encoding.value]

            if DatabaseSettingsName.case_sensitive.value in settings:
                self._case_sensitive = bool(settings[DatabaseSettingsName.case_sensitive.value])

            if DatabaseSettingsName.echo.value in settings:
                self._echo = bool(settings[DatabaseSettingsName.echo.value])
        except Exception as e:
            Console.set_foreground_color(ForegroundColor.red)
            Console.write_line(f'[ ERROR ] [ {__name__} ]: Reading error in {self.__name__} settings')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
            Console.set_foreground_color(ForegroundColor.default)
