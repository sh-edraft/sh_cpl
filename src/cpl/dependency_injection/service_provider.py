from collections import Callable
from typing import Optional

from cpl.dependency_injection import ServiceProviderABC
from cpl.dependency_injection.service_descriptor import ServiceDescriptor
from cpl.dependency_injection.service_factory_abc import ServiceFactoryABC
from cpl.dependency_injection.service_lifetime_enum import ServiceLifetimeEnum


class ServiceProvider(ServiceProviderABC):

    def __init__(self, service_factory: ServiceFactoryABC):
        ServiceProviderABC.__init__(self)

        self._service_factory = service_factory

    def _find_service(self, service_type: type) -> [ServiceDescriptor]:
        for descriptor in self._service_factory.service_descriptors:
            if descriptor.service_type == service_type or issubclass(descriptor.service_type, service_type):
                return descriptor

        return None

    def get_service(self, service_type: type) -> Optional[Callable[object]]:
        result = self._find_service(service_type)

        if result is None:
            return None

        if result.implementation is not None:
            return result.implementation

        implementation = result.service_type()
        if result.lifetime == ServiceLifetimeEnum.singleton:
            result.implementation = implementation

        return implementation
