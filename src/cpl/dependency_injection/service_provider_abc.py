from abc import abstractmethod, ABC
from collections import Callable
from typing import Type

from cpl.database.context.database_context_abc import DatabaseContextABC
from cpl.dependency_injection.service_abc import ServiceABC


class ServiceProviderABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC for service providing
        """
        pass

    @abstractmethod
    def add_db_context(self, db_context: Type[DatabaseContextABC]):
        """
        Adds database context
        :param db_context:
        :return:
        """
        pass

    @abstractmethod
    def get_db_context(self) -> Callable[DatabaseContextABC]:
        """"
        Returns database context
        :return Callable[DatabaseContextABC]:
        """
        pass

    @abstractmethod
    def add_transient(self, service_type: Type, service: Callable = None):
        """
        Adds a service with transient lifetime
        :param service_type:
        :param service:
        :return:
        """
        pass

    @abstractmethod
    def add_scoped(self, service_type: Type, service: Callable = None):
        """
        Adds a service with scoped lifetime
        :param service_type:
        :param service:
        :return:
        """
        pass

    @abstractmethod
    def add_singleton(self, service_type: Type, service: Callable = None):
        """
        Adds a service with singleton lifetime
        :param service_type:
        :param service:
        :return:
        """
        pass

    @abstractmethod
    def get_service(self, instance_type: Type) -> Callable[ServiceABC]:
        """
        Returns instance of given type
        :param instance_type:
        :return:
        """
        pass

    @abstractmethod
    def remove_service(self, instance_type: type):
        """
        Removes service
        :param instance_type:
        :return:
        """
        pass
