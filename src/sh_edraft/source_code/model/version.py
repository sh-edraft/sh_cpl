from typing import Optional

from sh_edraft.source_code.model.version_enum import VersionEnum
from sh_edraft.configuration.model.configuration_model_base import ConfigurationModelBase


class Version(ConfigurationModelBase):

    def __init__(
            self,
            major: int = None,
            minor: int = None,
            micro: float = None
    ):
        self._major: Optional[int] = major
        self._minor: Optional[int] = minor
        self._micro: Optional[float] = micro

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
        self._micro = float(settings[VersionEnum.Micro.value])

    def to_dict(self) -> dict:
        return {
            VersionEnum.Major.value: self._major,
            VersionEnum.Minor.value: self._minor,
            VersionEnum.Micro.value: self._micro
        }
