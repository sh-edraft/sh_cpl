from abc import abstractmethod

from sh_edraft.service.base.service_base import ServiceBase


class PublisherBase(ServiceBase):

    @abstractmethod
    def __init__(self):
        ServiceBase.__init__(self)

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
    def publish(self) -> str: pass
