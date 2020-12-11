from abc import abstractmethod

from sqlalchemy import engine
from sqlalchemy.orm import session

from sh_edraft.service.base.service_base import ServiceBase


class DatabaseContextBase(ServiceBase):

    @abstractmethod
    def __init__(self):
        ServiceBase.__init__(self)

    @property
    @abstractmethod
    def engine(self) -> engine: pass

    @property
    @abstractmethod
    def session(self) -> session: pass

    @abstractmethod
    def connect(self, connection_string: str): pass

    @abstractmethod
    def _create_tables(self): pass
