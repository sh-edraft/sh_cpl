from abc import abstractmethod

from sh_edraft.service.base.service_base import ServiceBase


class DatabaseConnectionBase(ServiceBase):

    @abstractmethod
    def __init__(self):
        ServiceBase.__init__(self)

    @abstractmethod
    def use_mysql(self, connection_string: str): pass
