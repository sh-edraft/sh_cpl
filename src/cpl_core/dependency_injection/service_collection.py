from typing import Union, Type, Callable, Optional

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.database.database_settings import DatabaseSettings
from cpl_core.database.context.database_context_abc import DatabaseContextABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.dependency_injection.service_descriptor import ServiceDescriptor
from cpl_core.dependency_injection.service_lifetime_enum import ServiceLifetimeEnum
from cpl_core.dependency_injection.service_provider import ServiceProvider
from cpl_core.logging.logger_service import Logger
from cpl_core.logging.logger_abc import LoggerABC
from cpl_core.utils.credential_manager import CredentialManager


class ServiceCollection(ServiceCollectionABC):
    r"""Representation of the collection of services"""

    def __init__(self, config: ConfigurationABC):
        ServiceCollectionABC.__init__(self)
        self._configuration: ConfigurationABC = config

        self._database_context: Optional[DatabaseContextABC] = None
        self._service_descriptors: list[ServiceDescriptor] = []

    def _add_descriptor(self, service: Union[type, object], lifetime: ServiceLifetimeEnum):
        found = False
        for descriptor in self._service_descriptors:
            if isinstance(service, descriptor.service_type):
                found = True

        if found:
            service_type = service
            if not isinstance(service, type):
                service_type = type(service)

            raise Exception(f'Service of type {service_type} already exists')

        self._service_descriptors.append(ServiceDescriptor(service, lifetime))

    def add_db_context(self, db_context_type: Type[DatabaseContextABC], db_settings: DatabaseSettings):
        self._database_context = db_context_type(db_settings)
        self._database_context.connect(db_settings)

    def add_logging(self):
        self.add_singleton(LoggerABC, Logger)

    def add_singleton(self, service_type: Union[type, object], service: Union[type, object] = None):
        impl = None
        if service is not None:
            if isinstance(service, type):
                impl = self.build_service_provider().build_service(service)

            self._add_descriptor(impl, ServiceLifetimeEnum.singleton)
        else:
            if isinstance(service_type, type):
                impl = self.build_service_provider().build_service(service_type)

            self._add_descriptor(impl, ServiceLifetimeEnum.singleton)

    def add_scoped(self, service_type: Type, service: Callable = None):
        if service is not None:
            self._add_descriptor(service, ServiceLifetimeEnum.scoped)
        else:
            self._add_descriptor(service_type, ServiceLifetimeEnum.scoped)
        

    def add_transient(self, service_type: type, service: type = None):
        if service is not None:
            self._add_descriptor(service, ServiceLifetimeEnum.transient)
        else:
            self._add_descriptor(service_type, ServiceLifetimeEnum.transient)

    def build_service_provider(self) -> ServiceProviderABC:
        return ServiceProvider(self._service_descriptors, self._configuration, self._database_context)
