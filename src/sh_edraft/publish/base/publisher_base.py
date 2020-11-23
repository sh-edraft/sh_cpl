from abc import abstractmethod

from sh_edraft.service.base import ServiceBase


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
    def publish(self) -> str: pass
