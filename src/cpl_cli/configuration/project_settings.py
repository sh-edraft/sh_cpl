import traceback
from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColor
from cpl_cli.configuration.version import Version
from cpl_cli.configuration.project_settings_name import ProjectSettingsName


class ProjectSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self._name: Optional[str] = None
        self._version: Optional[Version] = Version()
        self._author: Optional[str] = None
        self._author_email: Optional[str] = None
        self._description: Optional[str] = None
        self._long_description: Optional[str] = None
        self._url: Optional[str] = None
        self._copyright_date: Optional[str] = None
        self._copyright_name: Optional[str] = None
        self._license_name: Optional[str] = None
        self._license_description: Optional[str] = None
        self._dependencies: Optional[list[str]] = None
        self._python_version: Optional[str] = None
        
    @property
    def name(self):
        return self._name

    @property
    def version(self) -> Version:
        return self._version

    @property
    def author(self) -> str:
        return self._author

    @property
    def author_email(self) -> str:
        return self._author_email
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def long_description(self) -> str:
        return self._long_description
    
    @property
    def url(self) -> str:
        return self._url
    
    @property
    def copyright_date(self) -> str:
        return self._copyright_date
    
    @property
    def copyright_name(self) -> str:
        return self._copyright_name
    
    @property
    def license_name(self) -> str:
        return self._license_name
    
    @property
    def license_description(self) -> str:
        return self._license_description

    @property
    def dependencies(self) -> list[str]:
        return self._dependencies
    
    @property
    def python_version(self) -> str:
        return self._python_version

    def from_dict(self, settings: dict):
        try:
            self._name = settings[ProjectSettingsName.name.value]
            self._version.from_dict(settings[ProjectSettingsName.version.value])
            self._author = settings[ProjectSettingsName.author.value]
            self._author_email = settings[ProjectSettingsName.author_email.value]
            self._description = settings[ProjectSettingsName.description.value]
            self._long_description = settings[ProjectSettingsName.long_description.value]
            self._url = settings[ProjectSettingsName.url.value]
            self._copyright_date = settings[ProjectSettingsName.copyright_date.value]
            self._copyright_name = settings[ProjectSettingsName.copyright_name.value]
            self._license_name = settings[ProjectSettingsName.license_name.value]
            self._license_description = settings[ProjectSettingsName.license_description.value]
            self._dependencies = settings[ProjectSettingsName.dependencies.value]
            self._python_version = settings[ProjectSettingsName.python_version.value]
        except Exception as e:
            Console.set_foreground_color(ForegroundColor.red)
            Console.write_line(
                f'[ ERROR ] [ {__name__} ]: Reading error in {ProjectSettings.__name__} settings')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
            Console.set_foreground_color(ForegroundColor.default)
