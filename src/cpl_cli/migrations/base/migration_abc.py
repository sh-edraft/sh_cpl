from abc import ABC, abstractmethod


class MigrationABC(ABC):

    @abstractmethod
    def __init__(self, version: str):
        self._version = version

    @property
    def version(self) -> str:
        return self._version

    @abstractmethod
    def migrate(self): pass
