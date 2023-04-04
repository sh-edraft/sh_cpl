from typing import Optional

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_cli.configuration.version_settings_name_enum import VersionSettingsNameEnum


class VersionSettings(ConfigurationModelABC):
    def __init__(self, major: str = None, minor: str = None, micro: str = None):
        ConfigurationModelABC.__init__(self)

        self._major: Optional[str] = major
        self._minor: Optional[str] = minor
        self._micro: Optional[str] = micro

    @property
    def major(self) -> str:
        return self._major

    @property
    def minor(self) -> str:
        return self._minor

    @property
    def micro(self) -> str:
        return self._micro

    def to_str(self) -> str:
        if self._micro is None:
            return f"{self._major}.{self._minor}"
        else:
            return f"{self._major}.{self._minor}.{self._micro}"

    def from_dict(self, settings: dict):
        self._major = settings[VersionSettingsNameEnum.major.value]
        self._minor = settings[VersionSettingsNameEnum.minor.value]
        micro = settings[VersionSettingsNameEnum.micro.value]
        if micro != "":
            self._micro = micro

    def to_dict(self) -> dict:
        version = {
            VersionSettingsNameEnum.major.value: self._major,
            VersionSettingsNameEnum.minor.value: self._minor,
        }

        if self._micro is not None:
            version[VersionSettingsNameEnum.micro.value] = self._micro

        return version
