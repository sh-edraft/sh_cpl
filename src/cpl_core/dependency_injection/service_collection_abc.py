from abc import abstractmethod, ABC
from collections.abc import Callable
from typing import Type

from cpl_core.database.database_settings import DatabaseSettings
from cpl_core.database.context.database_context_abc import DatabaseContextABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.type import T


class ServiceCollectionABC(ABC):
    r"""ABC for the class :class:`cpl_core.dependency_injection.service_collection.ServiceCollection`"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_db_context(self, db_context_type: Type[DatabaseContextABC], db_settings: DatabaseSettings):
        r"""Adds database context

        Parameter
        ---------
            db_context: Type[:class:`cpl_core.database.context.database_context_abc.DatabaseContextABC`]
                Database context
        """
        pass

    @abstractmethod
    def add_logging(self):
        r"""Adds the CPL internal logger"""
        pass

    @abstractmethod
    def add_pipes(self):
        r"""Adds the CPL internal pipes as transient"""
        pass

    def add_discord(self):
        r"""Adds the CPL discord"""
        raise NotImplementedError('You should install and use the cpl-discord package')
        pass

    def add_translation(self):
        r"""Adds the CPL translation"""
        raise NotImplementedError('You should install and use the cpl-translation package')
        pass

    @abstractmethod
    def add_transient(self, service_type: T, service: T = None) -> 'ServiceCollectionABC':
        r"""Adds a service with transient lifetime

        Parameter
        ---------
            service_type: :class:`Type`
                Type of the service
            service: :class:`Callable`
                Object of the service

        Returns
        ------
            self: :class:`cpl_core.dependency_injection.service_collection_abc.ServiceCollectionABC
        """
        pass

    @abstractmethod
    def add_scoped(self, service_type: T, service: T = None) -> 'ServiceCollectionABC':
        r"""Adds a service with scoped lifetime

        Parameter
        ---------
            service_type: :class:`Type`
                Type of the service
            service: :class:`Callable`
                Object of the service

        Returns
        ------
            self: :class:`cpl_core.dependency_injection.service_collection_abc.ServiceCollectionABC
        """
        pass

    @abstractmethod
    def add_singleton(self, service_type: T, service: T = None) -> 'ServiceCollectionABC':
        r"""Adds a service with singleton lifetime

        Parameter
        ---------
            service_type: :class:`Type`
                Type of the service
            service: :class:`Callable`
                Object of the service

        Returns
        ------
            self: :class:`cpl_core.dependency_injection.service_collection_abc.ServiceCollectionABC
        """
        pass

    @abstractmethod
    def build_service_provider(self) -> ServiceProviderABC:
        r"""Creates instance of the service provider

        Returns
        -------
            Object of type :class:`cpl_core.dependency_injection.service_provider_abc.ServiceProviderABC`
        """
        pass
