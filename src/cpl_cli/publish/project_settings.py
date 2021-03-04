import traceback
from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.console.console import Console
from cpl.console.foreground_color import ForegroundColor
from cpl.version.version import Version
from cpl_cli.publish.project_settings_name import ProjectSettingsName


class ProjectSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self._dist_path: Optional[str] = None
        self._excluded_files: list[str] = []
        self._version: Optional[Version] = None

    @property
    def excluded_files(self) -> list[str]:
        return self._excluded_files

    @property
    def dist_path(self) -> str:
        return self._dist_path

    @dist_path.setter
    def dist_path(self, dist_path: str):
        self._dist_path = dist_path

    @property
    def version(self) -> Version:
        return self._version

    def from_dict(self, settings: dict):
        try:
            self._dist_path = settings[ProjectSettingsName.dist_path.value]
            self._excluded_files = settings[ProjectSettingsName.excluded_files.value]
            self._version = settings[ProjectSettingsName.version.value]
        except Exception as e:
            Console.set_foreground_color(ForegroundColor.red)
            Console.write_line(
                f'[ ERROR ] [ {__name__} ]: Reading error in {ProjectSettingsName.project.value} settings')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
            Console.set_foreground_color(ForegroundColor.default)
