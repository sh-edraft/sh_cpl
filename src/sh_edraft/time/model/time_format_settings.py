import traceback
from typing import Optional

from sh_edraft.configuration.base.configuration_model_base import ConfigurationModelBase
from sh_edraft.time.model.time_format_settings_names import TimeFormatSettingsNames
from sh_edraft.utils.console import Console


class TimeFormatSettings(ConfigurationModelBase):

    def __init__(self):
        self._date_format: Optional[str] = None
        self._time_format: Optional[str] = None
        self._date_time_format: Optional[str] = None
        self._date_time_log_format: Optional[str] = None
        self._os_name: Optional[str] = None
        self._hostname: Optional[str] = None

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
            Console.write_line(f'[ ERROR ] [ {__name__} ]: Reading error in {TimeFormatSettingsNames.formats.value} settings')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}', 'red')
