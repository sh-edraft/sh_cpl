from typing import Union, Type, Callable, Optional

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.database.context.database_context_abc import DatabaseContextABC
from cpl_core.database.database_settings import DatabaseSettings
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.dependency_injection.service_descriptor import ServiceDescriptor
from cpl_core.dependency_injection.service_lifetime_enum import ServiceLifetimeEnum
from cpl_core.dependency_injection.service_provider import ServiceProvider
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.logging.logger_abc import LoggerABC
from cpl_core.logging.logger_service import Logger
from cpl_core.pipes.pipe_abc import PipeABC
from cpl_core.type import T


class ServiceCollection(ServiceCollectionABC):
    r"""Representation of the collection of services"""

    def __init__(self, config: ConfigurationABC):
        ServiceCollectionABC.__init__(self)
        self._configuration: ConfigurationABC = config

        self._database_context: Optional[DatabaseContextABC] = None
        self._service_descriptors: list[ServiceDescriptor] = []

    def _add_descriptor(self, service: Union[type, object], lifetime: ServiceLifetimeEnum, base_type: Callable = None):
        found = False
        for descriptor in self._service_descriptors:
            if isinstance(service, descriptor.service_type):
                found = True

        if found:
            service_type = service
            if not isinstance(service, type):
                service_type = type(service)

            raise Exception(f"Service of type {service_type} already exists")

        self._service_descriptors.append(ServiceDescriptor(service, lifetime, base_type))

    def _add_descriptor_by_lifetime(self, service_type: Type, lifetime: ServiceLifetimeEnum, service: Callable = None):
        if service is not None:
            self._add_descriptor(service, lifetime, service_type)
        else:
            self._add_descriptor(service_type, lifetime)

        return self

    def add_db_context(self, db_context_type: Type[DatabaseContextABC], db_settings: DatabaseSettings):
        self.add_singleton(DatabaseContextABC, db_context_type)
        self._database_context = self.build_service_provider().get_service(DatabaseContextABC)
        self._database_context.connect(db_settings)

    def add_logging(self):
        self.add_singleton(LoggerABC, Logger)
        return self

    def add_pipes(self):
        for pipe in PipeABC.__subclasses__():
            self.add_transient(PipeABC, pipe)
        return self

    def add_singleton(self, service_type: Type[T], service: T = None):
        self._add_descriptor_by_lifetime(service_type, ServiceLifetimeEnum.singleton, service)
        return self

    def add_scoped(self, service_type: Type[T], service: Callable = None):
        self._add_descriptor_by_lifetime(service_type, ServiceLifetimeEnum.scoped, service)
        return self

    def add_transient(self, service_type: Type[T], service: T = None):
        self._add_descriptor_by_lifetime(service_type, ServiceLifetimeEnum.transient, service)
        return self

    def build_service_provider(self) -> ServiceProviderABC:
        sp = ServiceProvider(self._service_descriptors, self._configuration, self._database_context)
        ServiceProviderABC.set_global_provider(sp)
        return sp
