from abc import abstractmethod, ABC
from collections import Callable
from typing import Type

from cpl.database.context.database_context_abc import DatabaseContextABC
from cpl.dependency_injection.service_abc import ServiceABC


class ServiceProviderABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def add_db_context(self, db_context: Type[DatabaseContextABC]): pass

    @abstractmethod
    def get_db_context(self) -> Callable[DatabaseContextABC]: pass

    @abstractmethod
    def add_transient(self, service_type: Type, service: Type): pass

    @abstractmethod
    def add_scoped(self, service_type: Type, service: Type): pass

    @abstractmethod
    def add_singleton(self, service_type: Type, service: Callable): pass

    @abstractmethod
    def get_service(self, instance_type: Type) -> Callable[ServiceABC]: pass

    @abstractmethod
    def remove_service(self, instance_type: type): pass
