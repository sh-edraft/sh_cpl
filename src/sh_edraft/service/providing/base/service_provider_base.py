from abc import abstractmethod, ABC
from collections import Callable
from typing import Type

from sh_edraft.database.context.base.database_context_base import DatabaseContextBase
from sh_edraft.service.base.service_base import ServiceBase


class ServiceProviderBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def add_db_context(self, db_context: Type[DatabaseContextBase]): pass

    @abstractmethod
    def get_db_context(self) -> Callable[DatabaseContextBase]: pass

    @abstractmethod
    def add_transient(self, service_type: Type[ServiceBase], service: Type[ServiceBase]): pass

    @abstractmethod
    def add_scoped(self, service_type: Type[ServiceBase], service: Type[ServiceBase]): pass

    @abstractmethod
    def add_singleton(self, service_type: Type[ServiceBase], service: Callable[ServiceBase]): pass

    @abstractmethod
    def get_service(self, instance_type: Type[ServiceBase]) -> Callable[ServiceBase]: pass

    @abstractmethod
    def remove_service(self, instance_type: type): pass
