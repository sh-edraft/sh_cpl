from collections import Callable
from inspect import signature, Parameter
from typing import Optional

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.database.context.database_context_abc import DatabaseContextABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.dependency_injection.service_descriptor import ServiceDescriptor
from cpl_core.dependency_injection.service_lifetime_enum import ServiceLifetimeEnum
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC


class ServiceProvider(ServiceProviderABC):
    r"""Provider for the services

    Parameter
    ---------
        service_descriptors: list[:class:`cpl_core.dependency_injection.service_descriptor.ServiceDescriptor`]
            Descriptor of the service
        config: :class:`cpl_core.configuration.configuration_abc.ConfigurationABC`
            CPL Configuration
        db_context: Optional[:class:`cpl_core.database.context.database_context_abc.DatabaseContextABC`]
            Database representation
    """

    def __init__(self, service_descriptors: list[ServiceDescriptor], config: ConfigurationABC, db_context: Optional[DatabaseContextABC]):
        ServiceProviderABC.__init__(self)

        self._service_descriptors: list[ServiceDescriptor] = service_descriptors
        self._configuration: ConfigurationABC = config
        self._database_context = db_context

    def _find_service(self, service_type: type) -> [ServiceDescriptor]:
        for descriptor in self._service_descriptors:
            if descriptor.service_type == service_type or issubclass(descriptor.service_type, service_type):
                return descriptor

        return None

    def _get_service(self, parameter: Parameter) -> object:
        for descriptor in self._service_descriptors:
            if descriptor.service_type == parameter.annotation or issubclass(descriptor.service_type, parameter.annotation):
                if descriptor.implementation is not None:
                    return descriptor.implementation

                implementation = self.build_service(descriptor.service_type)
                if descriptor.lifetime == ServiceLifetimeEnum.singleton:
                    descriptor.implementation = implementation

                return implementation

    def build_service(self, service_type: type) -> object:
        for descriptor in self._service_descriptors:
            if descriptor.service_type == service_type or issubclass(descriptor.service_type, service_type):
                if descriptor.implementation is not None:
                    service_type = type(descriptor.implementation)
                else:
                    service_type = descriptor.service_type

                break

        sig = signature(service_type.__init__)
        params = []
        for param in sig.parameters.items():
            parameter = param[1]
            if parameter.name != 'self' and parameter.annotation != Parameter.empty:
                if issubclass(parameter.annotation, ServiceProviderABC):
                    params.append(self)

                elif issubclass(parameter.annotation, ApplicationEnvironmentABC):
                    params.append(self._configuration.environment)

                elif issubclass(parameter.annotation, DatabaseContextABC):
                    params.append(self._database_context)

                elif issubclass(parameter.annotation, ConfigurationModelABC):
                    params.append(self._configuration.get_configuration(parameter.annotation))

                elif issubclass(parameter.annotation, ConfigurationABC):
                    params.append(self._configuration)

                else:
                    params.append(self._get_service(parameter))

        return service_type(*params)

    def get_service(self, service_type: type) -> Optional[Callable[object]]:
        result = self._find_service(service_type)

        if result is None:
            return None

        if result.implementation is not None:
            return result.implementation

        implementation = self.build_service(service_type)
        if result.lifetime == ServiceLifetimeEnum.singleton:
            result.implementation = implementation

        return implementation
