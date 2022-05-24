from typing import Union, Optional

from cpl_core.console import Console
from cpl_core.dependency_injection.service_lifetime_enum import ServiceLifetimeEnum


class ServiceDescriptor:
    r"""Descriptor of a service

    Parameter
    ---------
        implementation: Union[:class:`type`, Optional[:class:`object`]]
            Object or type of service
        lifetime: :class:`cpl_core.dependency_injection.service_lifetime_enum.ServiceLifetimeEnum`
            Lifetime of the service
    """

    def __init__(self, implementation: Union[type, Optional[object]], lifetime: ServiceLifetimeEnum, base_type=None):

        self._service_type = implementation
        self._implementation = implementation
        self._lifetime = lifetime

        if not isinstance(implementation, type):
            self._service_type = type(implementation)
        else:
            self._implementation = None

        self._base_type = base_type if base_type is not None else self._service_type

    @property
    def service_type(self) -> type:
        return self._service_type

    @property
    def base_type(self) -> type:
        return self._base_type

    @property
    def implementation(self) -> Union[type, Optional[object]]:
        return self._implementation

    @implementation.setter
    def implementation(self, implementation: Union[type, Optional[object]]):
        self._implementation = implementation

    @property
    def lifetime(self) -> ServiceLifetimeEnum:
        return self._lifetime
