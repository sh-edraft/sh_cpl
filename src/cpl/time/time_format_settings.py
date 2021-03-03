import traceback
from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.console.console import Console
from cpl.console.foreground_color import ForegroundColor
from cpl.time.time_format_settings_names import TimeFormatSettingsNames


class TimeFormatSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)
        self._date_format: Optional[str] = None
        self._time_format: Optional[str] = None
        self._date_time_format: Optional[str] = None
        self._date_time_log_format: Optional[str] = None

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

    def from_dict(self, settings: dict):
        try:
            self._date_format = settings[TimeFormatSettingsNames.date_format.value]
            self._time_format = settings[TimeFormatSettingsNames.time_format.value]
            self._date_time_format = settings[TimeFormatSettingsNames.date_time_format.value]
            self._date_time_log_format = settings[TimeFormatSettingsNames.date_time_log_format.value]
        except Exception as e:
            Console.set_foreground_color(ForegroundColor.red)
            Console.write_line(f'[ ERROR ] [ {__name__} ]: Reading error in {self.__name__} settings')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
            Console.set_foreground_color(ForegroundColor.default)
