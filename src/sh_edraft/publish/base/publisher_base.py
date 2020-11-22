from abc import ABC, abstractmethod


class PublisherBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def source_path(self) -> str: pass

    @property
    @abstractmethod
    def dist_path(self) -> str: pass

    @abstractmethod
    def publish(self) -> str: pass
