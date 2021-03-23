from typing import Union, Type, Callable, Optional

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.database.context import DatabaseContextABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl.dependency_injection.service_descriptor import ServiceDescriptor
from cpl.dependency_injection.service_lifetime_enum import ServiceLifetimeEnum
from cpl.dependency_injection.service_provider import ServiceProvider


class ServiceCollection(ServiceCollectionABC):

    def __init__(self, config: ConfigurationABC, runtime: ApplicationRuntimeABC):
        ServiceCollectionABC.__init__(self)
        self._configuration: ConfigurationABC = config
        self._runtime: ApplicationRuntimeABC = runtime

        self._database_context: Optional[DatabaseContextABC] = None
        self._service_descriptors: list[ServiceDescriptor] = []

    def _add_descriptor(self, service: Union[type, object], lifetime: ServiceLifetimeEnum):
        found = False
        for descriptor in self._service_descriptors:
            if not isinstance(service, type):
                service = type(service)

            if descriptor.service_type == service:
                found = True

        if found:
            service_type = service
            if not isinstance(service, type):
                service_type = type(service)

            raise Exception(f'Service of type {service_type} already exists')

        self._service_descriptors.append(ServiceDescriptor(service, lifetime))

    def add_db_context(self, db_context: Type[DatabaseContextABC]):
        pass

    def add_singleton(self, service_type: Union[type, object], service: Union[type, object] = None):
        if service is not None:
            if isinstance(service, type):
                service = self.build_service_provider().build_service(service)

            self._add_descriptor(service, ServiceLifetimeEnum.singleton)
        else:
            if isinstance(service_type, type):
                service_type = self.build_service_provider().build_service(service_type)

            self._add_descriptor(service_type, ServiceLifetimeEnum.singleton)

    def add_scoped(self, service_type: Type, service: Callable = None):
        pass

    def add_transient(self, service_type: Union[type], service: Union[type] = None):
        if service is not None:
            self._add_descriptor(service, ServiceLifetimeEnum.transient)
        else:
            self._add_descriptor(service_type, ServiceLifetimeEnum.transient)

    def build_service_provider(self) -> ServiceProviderABC:
        return ServiceProvider(self._service_descriptors, self._configuration, self._runtime)
