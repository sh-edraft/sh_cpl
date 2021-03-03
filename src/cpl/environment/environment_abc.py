from abc import ABC, abstractmethod


class EnvironmentABC(ABC):

    @abstractmethod
    def __init__(self): pass
    
    @property
    @abstractmethod
    def environment_name(self) -> str: pass
    
    @environment_name.setter
    @abstractmethod
    def environment_name(self, environment_name: str): pass
    
    @property
    @abstractmethod
    def application_name(self) -> str: pass
    
    @application_name.setter
    @abstractmethod
    def application_name(self, application_name: str): pass
    
    @property
    @abstractmethod
    def customer(self) -> str: pass
    
    @customer.setter
    @abstractmethod
    def customer(self, customer: str): pass

    @property
    @abstractmethod
    def content_root_path(self) -> str: pass

    @content_root_path.setter
    @abstractmethod
    def content_root_path(self, content_root_path: str): pass

    @property
    @abstractmethod
    def host_name(self) -> str: pass
