from abc import ABC, abstractmethod


class MigrationServiceABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def migrate_from(self, version: str):
        pass
