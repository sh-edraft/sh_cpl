import sys
import traceback
from typing import Optional

from cpl_cli.configuration.build_settings_name_enum import BuildSettingsNameEnum
from cpl_cli.configuration.project_type_enum import ProjectTypeEnum
from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum


class BuildSettings(ConfigurationModelABC):
    def __init__(
        self,
        project_type: ProjectTypeEnum = None,
        source_path: str = None,
        output_path: str = None,
        main: str = None,
        entry_point: str = None,
        include_package_data: bool = None,
        included: list[str] = None,
        excluded: list[str] = None,
        package_data: dict[str, list[str]] = None,
        project_references: list[str] = None,
    ):
        ConfigurationModelABC.__init__(self)

        self._project_type: Optional[ProjectTypeEnum] = project_type
        self._source_path: Optional[str] = source_path
        self._output_path: Optional[str] = output_path
        self._main: Optional[str] = main
        self._entry_point: Optional[str] = entry_point
        self._include_package_data: Optional[bool] = include_package_data
        self._included: Optional[list[str]] = included
        self._excluded: Optional[list[str]] = excluded
        self._package_data: Optional[dict[str, list[str]]] = package_data
        self._project_references: Optional[list[str]] = [] if project_references is None else project_references

        if sys.platform == "win32":
            self._source_path = str(self._source_path).replace("/", "\\")
            self._output_path = str(self._output_path).replace("/", "\\")

            # windows paths for excluded files
            excluded = []
            for ex in self._excluded:
                excluded.append(str(ex).replace("/", "\\"))

            self._excluded = excluded

            # windows paths for included files
            included = []
            for inc in self._included:
                included.append(str(inc).replace("/", "\\"))

            self._included = included

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
