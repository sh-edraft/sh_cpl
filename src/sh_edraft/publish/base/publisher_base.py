from abc import ABC, abstractmethod

from sh_edraft.publish.model.template import Template


class PublisherBase(ABC):

    @abstractmethod
    def __init__(self, source_path: str, dist_path: str, settings: list[Template]):
        self._source_path = source_path
        self._dist_path = dist_path
        self._settings = settings

    @property
    @abstractmethod
    def source_path(self) -> str:
        pass

    @property
    @abstractmethod
    def dist_path(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def publish(self):
        pass
