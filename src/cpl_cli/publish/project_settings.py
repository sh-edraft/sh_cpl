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

        self._name: Optional[str] = None
        self._author: Optional[str] = None
        self._description: Optional[str] = None
        self._long_description: Optional[str] = None
        self._copyright_date: Optional[str] = None
        self._copyright_name: Optional[str] = None
        self._license_name: Optional[str] = None
        self._license_description: Optional[str] = None
        self._version: Optional[Version] = Version()
        self._source_path: Optional[str] = None
        self._dist_path: Optional[str] = None
        self._included: list[str] = []
        self._excluded: list[str] = []

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def author(self) -> Optional[str]:
        return self._author

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def long_description(self) -> Optional[str]:
        return self._long_description

    @property
    def copyright_date(self) -> Optional[str]:
        return self._copyright_date

    @property
    def copyright_name(self) -> Optional[str]:
        return self._copyright_name

    @property
    def license_name(self) -> Optional[str]:
        return self._license_name

    @property
    def license_description(self) -> Optional[str]:
        return self._license_description

    @property
    def version(self) -> Optional[Version]:
        return self._version

    @property
    def source_path(self) -> str:
        return self._source_path

    @source_path.setter
    def source_path(self, source_path: str):
        self._source_path = source_path

    @property
    def dist_path(self) -> str:
        return self._dist_path

    @dist_path.setter
    def dist_path(self, dist_path: str):
        self._dist_path = dist_path

    @property
    def included(self) -> list[str]:
        return self._included

    @property
    def excluded(self) -> list[str]:
        return self._excluded

    def from_dict(self, settings: dict):
        try:
            self._name = settings[ProjectSettingsName.name.value]
            self._author = settings[ProjectSettingsName.author.value]
            self._description = settings[ProjectSettingsName.description.value]
            self._long_description = settings[ProjectSettingsName.long_description.value]
            self._copyright_date = settings[ProjectSettingsName.copyright_date.value]
            self._copyright_name = settings[ProjectSettingsName.copyright_name.value]
            self._license_name = settings[ProjectSettingsName.license_name.value]
            self._license_description = settings[ProjectSettingsName.license_description.value]
            self._version.from_dict(settings[ProjectSettingsName.version.value])
            self._source_path = settings[ProjectSettingsName.source_path.value]
            self._dist_path = settings[ProjectSettingsName.dist_path.value]
            self._included = settings[ProjectSettingsName.included.value]
            self._excluded = settings[ProjectSettingsName.excluded.value]
        except Exception as e:
            Console.set_foreground_color(ForegroundColor.red)
            Console.write_line(
                f'[ ERROR ] [ {__name__} ]: Reading error in {ProjectSettingsName.project.value} settings')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
            Console.set_foreground_color(ForegroundColor.default)
