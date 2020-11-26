import traceback
from typing import Optional

from sh_edraft.configuration.base.configuration_model_base import ConfigurationModelBase
from sh_edraft.logging.model.logging_settings_name import LogSettingsName
from sh_edraft.utils.console import Console
from sh_edraft.logging.model.logging_level import LoggingLevel


class LoggingSettings(ConfigurationModelBase):

    def __init__(self):
        ConfigurationModelBase.__init__(self)

        self._path: Optional[str] = None
        self._filename: Optional[str] = None
        self._console: Optional[LoggingLevel] = None
        self._level: Optional[LoggingLevel] = None

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        self._path = path

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, filename: str) -> None:
        self._filename = filename

    @property
    def console(self) -> LoggingLevel:
        return self._console

    @console.setter
    def console(self, console: LoggingLevel) -> None:
        self._console = console

    @property
    def level(self) -> LoggingLevel:
        return self._level

    @level.setter
    def level(self, level: LoggingLevel) -> None:
        self._level = level

    def from_dict(self, settings: dict):
        try:
            self._path = settings[LogSettingsName.path.value]
            self._filename = settings[LogSettingsName.filename.value]
            self._console = LoggingLevel[settings[LogSettingsName.console_level.value]]
            self._level = LoggingLevel[settings[LogSettingsName.file_level.value]]
        except Exception as e:
            Console.write_line(f'[ ERROR ] [ {__name__} ]: Reading error in {LogSettingsName.log.value} settings', 'red')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}', 'red')
