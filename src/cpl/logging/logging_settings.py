import traceback
from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.console.console import Console
from cpl.console.foreground_color import ForegroundColor
from cpl.logging.logging_level import LoggingLevel
from cpl.logging.logging_settings_name import LoggingSettingsName


class LoggingSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)
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
            self._path = settings[LoggingSettingsName.path.value]
            self._filename = settings[LoggingSettingsName.filename.value]
            self._console = LoggingLevel[settings[LoggingSettingsName.console_level.value]]
            self._level = LoggingLevel[settings[LoggingSettingsName.file_level.value]]
        except Exception as e:
            Console.set_foreground_color(ForegroundColor.red)
            Console.write_line(f'[ ERROR ] [ {__name__} ]: Reading error in {self.__name__} settings')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
            Console.set_foreground_color(ForegroundColor.default)
