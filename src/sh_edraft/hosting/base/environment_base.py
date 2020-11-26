from abc import ABC, abstractmethod

from sh_edraft.hosting.model.environment_name import EnvironmentName


class EnvironmentBase(ABC):

    @abstractmethod
    def __init__(self): pass
    
    @property
    @abstractmethod
    def name(self) -> EnvironmentName: pass
    
    @name.setter
    @abstractmethod
    def name(self, name: EnvironmentName): pass

    @property
    @abstractmethod
    def content_root_path(self) -> str: pass

    @content_root_path.setter
    @abstractmethod
    def content_root_path(self, content_root_path: str): pass
