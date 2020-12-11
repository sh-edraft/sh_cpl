from abc import abstractmethod

from sh_edraft.service.base import ServiceBase


class UserRepoBase(ServiceBase):

    @abstractmethod
    def __init__(self):
        ServiceBase.__init__(self)
