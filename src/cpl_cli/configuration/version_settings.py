from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_cli.configuration.version_settings_name_enum import VersionSettingsNameEnum


class VersionSettings(ConfigurationModelABC):

    def __init__(
            self,
            major: str = None,
            minor: str = None,
            micro: str = None
    ):
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
        return f'{self._major}.{self._minor}.{self._micro}'

    def from_dict(self, settings: dict):
        self._major = settings[VersionSettingsNameEnum.major.value]
        self._minor = settings[VersionSettingsNameEnum.minor.value]
        self._micro = settings[VersionSettingsNameEnum.micro.value]

    def to_dict(self) -> dict:
        return {
            VersionSettingsNameEnum.major.value: self._major,
            VersionSettingsNameEnum.minor.value: self._minor,
            VersionSettingsNameEnum.micro.value: self._micro
        }
