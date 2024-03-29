import traceback
from typing import Optional

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.logging.logging_level_enum import LoggingLevelEnum
from cpl_core.logging.logging_settings_name_enum import LoggingSettingsNameEnum


class LoggingSettings(ConfigurationModelABC):
    r"""Representation of logging settings"""

    def __init__(
        self,
        path: str = None,
        filename: str = None,
        console_log_level: LoggingLevelEnum = None,
        file_log_level: LoggingLevelEnum = None,
    ):
        ConfigurationModelABC.__init__(self)
        self._path: Optional[str] = path
        self._filename: Optional[str] = filename
        self._console: Optional[LoggingLevelEnum] = console_log_level
        self._level: Optional[LoggingLevelEnum] = file_log_level

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
