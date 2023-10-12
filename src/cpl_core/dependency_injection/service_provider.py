import copy
import typing
from inspect import signature, Parameter, Signature
from typing import Optional

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.database.context.database_context_abc import DatabaseContextABC
from cpl_core.dependency_injection.scope_abc import ScopeABC
from cpl_core.dependency_injection.scope_builder import ScopeBuilder
from cpl_core.dependency_injection.service_descriptor import ServiceDescriptor
from cpl_core.dependency_injection.service_lifetime_enum import ServiceLifetimeEnum
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_core.type import T


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

    def __init__(
        self,
        service_descriptors: list[ServiceDescriptor],
        config: ConfigurationABC,
        db_context: Optional[DatabaseContextABC],
    ):
        ServiceProviderABC.__init__(self)

        self._service_descriptors: list[ServiceDescriptor] = service_descriptors
        self._configuration: ConfigurationABC = config
        self._database_context = db_context
        self._scope: Optional[ScopeABC] = None

    def _find_service(self, service_type: type) -> Optional[ServiceDescriptor]:
        for descriptor in self._service_descriptors:
            if descriptor.service_type == service_type or issubclass(descriptor.base_type, service_type):
                return descriptor

        return None

    def _get_service(self, parameter: Parameter) -> Optional[object]:
        for descriptor in self._service_descriptors:
            if descriptor.service_type == parameter.annotation or issubclass(
                descriptor.service_type, parameter.annotation
            ):
                if descriptor.implementation is not None:
                    return descriptor.implementation

                implementation = self.build_service(descriptor.service_type)
                if descriptor.lifetime == ServiceLifetimeEnum.singleton:
                    descriptor.implementation = implementation

                return implementation

        # raise Exception(f'Service {parameter.annotation} not found')

    def _get_services(self, t: type, *args, **kwargs) -> list[Optional[object]]:
        implementations = []
        for descriptor in self._service_descriptors:
            if descriptor.service_type == t or issubclass(descriptor.service_type, t):
                if descriptor.implementation is not None:
                    implementations.append(descriptor.implementation)
                    continue

                implementation = self.build_service(descriptor.service_type, *args, **kwargs)
                if descriptor.lifetime == ServiceLifetimeEnum.singleton:
                    descriptor.implementation = implementation

                implementations.append(implementation)

        return implementations

    def build_by_signature(self, sig: Signature) -> list[T]:
        params = []
        for param in sig.parameters.items():
            parameter = param[1]
            if parameter.name != "self" and parameter.annotation != Parameter.empty:
                if typing.get_origin(parameter.annotation) == list:
                    params.append(self._get_services(typing.get_args(parameter.annotation)[0]))

                elif issubclass(parameter.annotation, ServiceProviderABC):
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

        return params

    def build_service(self, service_type: type, *args, **kwargs) -> object:
        for descriptor in self._service_descriptors:
            if descriptor.service_type == service_type or issubclass(descriptor.service_type, service_type):
                if descriptor.implementation is not None:
                    service_type = type(descriptor.implementation)
                else:
                    service_type = descriptor.service_type

                break

        sig = signature(service_type.__init__)
        params = self.build_by_signature(sig)

        return service_type(*params, *args, **kwargs)

    def set_scope(self, scope: ScopeABC):
        self._scope = scope

    def create_scope(self) -> ScopeABC:
        descriptors = []

        for descriptor in self._service_descriptors:
            if descriptor.lifetime == ServiceLifetimeEnum.singleton:
                descriptors.append(descriptor)
            else:
                descriptors.append(copy.deepcopy(descriptor))

        sb = ScopeBuilder(ServiceProvider(descriptors, self._configuration, self._database_context))
        return sb.build()

    def get_service(self, service_type: T, *args, **kwargs) -> Optional[T]:
        result = self._find_service(service_type)

        if result is None:
            return None

        if result.implementation is not None:
            return result.implementation

        implementation = self.build_service(service_type, *args, **kwargs)
        if (
            result.lifetime == ServiceLifetimeEnum.singleton
            or result.lifetime == ServiceLifetimeEnum.scoped
            and self._scope is not None
        ):
            result.implementation = implementation

        return implementation

    def get_services(self, service_type: T, *args, **kwargs) -> list[Optional[T]]:
        implementations = []

        if typing.get_origin(service_type) == list:
            raise Exception(f"Invalid type {service_type}! Expected single type not list of type")

        implementations.extend(self._get_services(service_type))

        return implementations
