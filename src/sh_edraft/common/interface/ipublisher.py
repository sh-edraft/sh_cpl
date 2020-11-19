from abc import ABC, abstractmethod
from typing import List

from sh_edraft.publish.model.template import Template


class IPublisher(ABC):

    @abstractmethod
    def __init__(self, local_path: str):
        pass

    @property
    @abstractmethod
    def local_path(self) -> str:
        pass

    @abstractmethod
    def create(self, templates: List[Template]):
        pass

    @abstractmethod
    def publish(self):
        pass
