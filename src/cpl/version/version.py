from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.version.version_enum import VersionEnum


class Version(ConfigurationModelABC):

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
        self._major = int(settings[VersionEnum.Major.value])
        self._minor = int(settings[VersionEnum.Minor.value])
        self._micro = int(settings[VersionEnum.Micro.value])

    def to_dict(self) -> dict:
        return {
            VersionEnum.Major.value: self._major,
            VersionEnum.Minor.value: self._minor,
            VersionEnum.Micro.value: self._micro
        }
