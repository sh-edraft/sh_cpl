import traceback
from typing import Optional

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.time.time_format_settings_names_enum import TimeFormatSettingsNamesEnum


class TimeFormatSettings(ConfigurationModelABC):
    r"""Representation of time format settings"""

    def __init__(
        self,
        date_format: str = None,
        time_format: str = None,
        date_time_format: str = None,
        date_time_log_format: str = None,
    ):
        ConfigurationModelABC.__init__(self)
        self._date_format: Optional[str] = date_format
        self._time_format: Optional[str] = time_format
        self._date_time_format: Optional[str] = date_time_format
        self._date_time_log_format: Optional[str] = date_time_log_format

    @property
    def date_format(self) -> str:
        return self._date_format

    @date_format.setter
    def date_format(self, date_format: str) -> None:
        self._date_format = date_format

    @property
    def time_format(self) -> str:
        return self._time_format

    @time_format.setter
    def time_format(self, time_format: str):
        self._time_format = time_format

    @property
    def date_time_format(self) -> str:
        return self._date_time_format

    @date_time_format.setter
    def date_time_format(self, date_time_format: str) -> None:
        self._date_time_format = date_time_format

    @property
    def date_time_log_format(self):
        return self._date_time_log_format

    @date_time_log_format.setter
    def date_time_log_format(self, date_time_now_format: str) -> None:
        self._date_time_log_format = date_time_now_format
