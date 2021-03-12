import traceback
from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.logging.logging_level_enum import LoggingLevelEnum
from cpl.logging.logging_settings_name_enum import LoggingSettingsNameEnum


class LoggingSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)
        self._path: Optional[str] = None
        self._filename: Optional[str] = None
        self._console: Optional[LoggingLevelEnum] = None
        self._level: Optional[LoggingLevelEnum] = None

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
    def console(self) -> LoggingLevelEnum:
        return self._console

    @console.setter
    def console(self, console: LoggingLevelEnum) -> None:
        self._console = console

    @property
    def level(self) -> LoggingLevelEnum:
        return self._level

    @level.setter
    def level(self, level: LoggingLevelEnum) -> None:
        self._level = level

    def from_dict(self, settings: dict):
        try:
            self._path = settings[LoggingSettingsNameEnum.path.value]
            self._filename = settings[LoggingSettingsNameEnum.filename.value]
            self._console = LoggingLevelEnum[settings[LoggingSettingsNameEnum.console_level.value]]
            self._level = LoggingLevelEnum[settings[LoggingSettingsNameEnum.file_level.value]]
        except Exception as e:
            Console.set_foreground_color(ForegroundColorEnum.red)
            Console.write_line(f'[ ERROR ] [ {__name__} ]: Reading error in {self.__name__} settings')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
            Console.set_foreground_color(ForegroundColorEnum.default)
