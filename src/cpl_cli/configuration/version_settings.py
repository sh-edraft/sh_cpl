from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_cli.configuration.version_settings_name_enum import VersionSettingsName


class VersionSettings(ConfigurationModelABC):

    def __init__(
            self,
            major: int = None,
            minor: int = None,
            micro: float = None
    ):
        ConfigurationModelABC.__init__(self)

        self._major: Optional[int] = major
        self._minor: Optional[int] = minor
        self._micro: Optional[int] = micro

    @property
    def major(self) -> int:
        return self._major

    @property
    def minor(self) -> int:
        return self._minor

    @property
    def micro(self) -> float:
        return self._micro

    def to_str(self) -> str:
        return f'{self._major}.{self._minor}.{self._micro}'

    def from_dict(self, settings: dict):
        self._major = int(settings[VersionSettingsName.major.value])
        self._minor = int(settings[VersionSettingsName.minor.value])
        self._micro = int(settings[VersionSettingsName.micro.value])

    def to_dict(self) -> dict:
        return {
            VersionSettingsName.major.value: self._major,
            VersionSettingsName.minor.value: self._minor,
            VersionSettingsName.micro.value: self._micro
        }
