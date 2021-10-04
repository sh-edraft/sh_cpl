import sys
import traceback
from typing import Optional

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_cli.configuration.build_settings_name_enum import BuildSettingsNameEnum
from cpl_cli.configuration.project_type_enum import ProjectTypeEnum


class BuildSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self._project_type: Optional[ProjectTypeEnum] = None
        self._source_path: Optional[str] = None
        self._output_path: Optional[str] = None
        self._main: Optional[str] = None
        self._entry_point: Optional[str] = None
        self._include_package_data: Optional[bool] = None
        self._included: Optional[list[str]] = None
        self._excluded: Optional[list[str]] = None
        self._package_data: Optional[dict[str, list[str]]] = None
        self._project_references: Optional[list[str]] = None

    @property
    def project_type(self):
        return self._project_type

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

    @property
    def project_references(self) -> list[str]:
        return self._project_references

    def from_dict(self, settings: dict):
        try:
            self._project_type = settings[BuildSettingsNameEnum.project_type.value]
            self._source_path = settings[BuildSettingsNameEnum.source_path.value]
            self._output_path = settings[BuildSettingsNameEnum.output_path.value]
            self._include_package_data = bool(settings[BuildSettingsNameEnum.include_package_data.value])
            self._main = settings[BuildSettingsNameEnum.main.value]
            self._entry_point = settings[BuildSettingsNameEnum.entry_point.value]
            self._included = settings[BuildSettingsNameEnum.included.value]
            self._excluded = settings[BuildSettingsNameEnum.excluded.value]
            self._package_data = settings[BuildSettingsNameEnum.package_data.value]

            if BuildSettingsNameEnum.project_references.value in settings:
                self._project_references = settings[BuildSettingsNameEnum.project_references.value]
            else:
                self._project_references = []

            if sys.platform == 'win32':
                self._source_path = str(self._source_path).replace('/', '\\')
                self._output_path = str(self._output_path).replace('/', '\\')

                # windows paths for excluded files
                excluded = []
                for ex in self._excluded:
                    excluded.append(str(ex).replace('/', '\\'))

                self._excluded = excluded

                # windows paths for included files
                included = []
                for inc in self._included:
                    included.append(str(inc).replace('/', '\\'))

                self._included = included

        except Exception as e:
            Console.set_foreground_color(ForegroundColorEnum.red)
            Console.write_line(
                f'[ ERROR ] [ {__name__} ]: Reading error in {BuildSettings.__name__} settings')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
            Console.set_foreground_color(ForegroundColorEnum.default)
