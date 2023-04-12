import os
import sys
from typing import Optional

from cpl_cli.configuration.project_settings_name_enum import ProjectSettingsNameEnum
from cpl_cli.configuration.version_settings import VersionSettings
from cpl_cli.error import Error
from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC


class ProjectSettings(ConfigurationModelABC):
    def __init__(
        self,
        name: str = None,
        version: VersionSettings = None,
        author: str = None,
        author_email: str = None,
        description: str = None,
        long_description: str = None,
        url: str = None,
        copyright_date: str = None,
        copyright_name: str = None,
        license_name: str = None,
        license_description: str = None,
        dependencies: list = None,
        dev_dependencies: list = None,
        python_version: str = None,
        python_path: dict = None,
        python_executable: str = None,
        classifiers: list = None,
    ):
        ConfigurationModelABC.__init__(self)

        self._name: Optional[str] = name
        self._version: Optional[VersionSettings] = version
        self._author: Optional[str] = author
        self._author_email: Optional[str] = author_email
        self._description: Optional[str] = description
        self._long_description: Optional[str] = long_description
        self._url: Optional[str] = url
        self._copyright_date: Optional[str] = copyright_date
        self._copyright_name: Optional[str] = copyright_name
        self._license_name: Optional[str] = license_name
        self._license_description: Optional[str] = license_description
        self._dependencies: Optional[list[str]] = [] if dependencies is None else dependencies
        self._dev_dependencies: Optional[list[str]] = [] if dev_dependencies is None else dev_dependencies
        self._python_version: Optional[str] = python_version
        self._python_path: Optional[str] = python_path
        self._python_executable: Optional[str] = python_executable
        self._classifiers: Optional[list[str]] = [] if classifiers is None else classifiers

        if python_path is not None and sys.platform in python_path:
            path = f"{python_path[sys.platform]}"

            if path == "" or path is None:
                Error.warn(f"{ProjectSettingsNameEnum.python_path.value} not set")
                path = sys.executable
            else:
                if not path.endswith("bin/python"):
                    path = os.path.join(path, "bin/python")
        else:
            path = sys.executable

        self._python_executable = path

    @property
    def name(self):
        return self._name

    @property
    def version(self) -> VersionSettings:
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
    def dev_dependencies(self) -> list[str]:
        return self._dev_dependencies

    @property
    def python_version(self) -> str:
        return self._python_version

    @property
    def python_path(self) -> str:
        return self._python_path

    @property
    def python_executable(self) -> str:
        return self._python_executable

    @property
    def classifiers(self) -> list[str]:
        return self._classifiers
