from abc import abstractmethod, ABC
from collections import Callable
from typing import Type

from cpl.database.database_settings import DatabaseSettings
from cpl.database.context.database_context_abc import DatabaseContextABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC


class ServiceCollectionABC(ABC):
    r"""ABC for the class :class:`cpl.dependency_injection.service_collection.ServiceCollection`"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_db_context(self, db_context: Type[DatabaseContextABC], db_settings: DatabaseSettings):
        r"""Adds database context

        Parameter
        ---------
            db_context: Type[:class:`cpl.database.context.database_context_abc.DatabaseContextABC`]
                Database context
            db_settings: :class:`cpl.database.database_settings.DatabaseSettings`
                Database settings
        """
        pass

    @abstractmethod
    def add_logging(self):
        r"""Adds the CPL internal logger"""
        pass

    @abstractmethod
    def add_transient(self, service_type: Type, service: Callable = None):
        r"""Adds a service with transient lifetime

        Parameter
        ---------
            service_type: :class:`Type`
                Type of the service
            service: :class:`Callable`
                Object of the service
        """
        pass

    @abstractmethod
    def add_scoped(self, service_type: Type, service: Callable = None):
        r"""Adds a service with scoped lifetime

        Parameter
        ---------
            service_type: :class:`Type`
                Type of the service
            service: :class:`Callable`
                Object of the service
        """
        pass

    @abstractmethod
    def add_singleton(self, service_type: Type, service: Callable = None):
        r"""Adds a service with singleton lifetime

        Parameter
        ---------
            service_type: :class:`Type`
                Type of the service
            service: :class:`Callable`
                Object of the service
        """
        pass

    @abstractmethod
    def build_service_provider(self) -> ServiceProviderABC:
        r"""Creates instance of the service provider

        Returns
        -------
            Object of type :class:`cpl.dependency_injection.service_provider_abc.ServiceProviderABC`
        """
        pass
