import traceback
from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl_cli.configuration.build_settings_name_enum import BuildSettingsName


class BuildSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self._source_path: Optional[str] = None
        self._output_path: Optional[str] = None
        self._main: Optional[str] = None
        self._entry_point: Optional[str] = None
        self._include_package_data: Optional[bool] = None
        self._included: Optional[list[str]] = None
        self._excluded: Optional[list[str]] = None
        self._package_data: Optional[dict[str, list[str]]] = None

    @property
    def source_path(self) -> str:
        return self._source_path

    @property
    def output_path(self) -> str:
        return self._output_path

    @property
    def main(self) -> str:
        return self._main

    @property
    def entry_point(self) -> str:
        return self._entry_point

    @property
    def include_package_data(self) -> bool:
        return self._include_package_data

    @property
    def included(self) -> list[str]:
        return self._included

    @property
    def excluded(self) -> list[str]:
        return self._excluded

    @property
    def package_data(self) -> dict[str, list[str]]:
        return self._package_data

    def from_dict(self, settings: dict):
        try:
            self._source_path = settings[BuildSettingsName.source_path.value]
            self._output_path = settings[BuildSettingsName.output_path.value]
            self._include_package_data = bool(settings[BuildSettingsName.include_package_data.value])
            self._main = settings[BuildSettingsName.main.value]
            self._entry_point = settings[BuildSettingsName.entry_point.value]
            self._included = settings[BuildSettingsName.included.value]
            self._excluded = settings[BuildSettingsName.excluded.value]
            self._package_data = settings[BuildSettingsName.package_data.value]
        except Exception as e:
            Console.set_foreground_color(ForegroundColorEnum.red)
            Console.write_line(
                f'[ ERROR ] [ {__name__} ]: Reading error in {BuildSettings.__name__} settings')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
            Console.set_foreground_color(ForegroundColorEnum.default)
