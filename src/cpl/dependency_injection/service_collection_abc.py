from abc import abstractmethod, ABC
from collections import Callable
from typing import Type

from cpl.database.context.database_context_abc import DatabaseContextABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class ServiceCollectionABC(ABC):

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
    def build_service_provider(self) -> ServiceProviderABC:
        """
        Creates instance of the service provider
        """
        pass
