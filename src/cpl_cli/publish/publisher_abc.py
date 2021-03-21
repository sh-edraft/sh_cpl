from abc import abstractmethod

from cpl.dependency_injection.service_abc import ServiceABC


class PublisherABC(ServiceABC):

    @abstractmethod
    def __init__(self):
        ServiceABC.__init__(self)

    @property
    @abstractmethod
    def source_path(self) -> str: pass

    @property
    @abstractmethod
    def dist_path(self) -> str: pass

    @abstractmethod
    def include(self, path: str): pass

    @abstractmethod
    def exclude(self, path: str): pass

    @abstractmethod
    def build(self): pass

    @abstractmethod
    def publish(self): pass
