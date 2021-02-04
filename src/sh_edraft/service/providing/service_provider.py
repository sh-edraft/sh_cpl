from collections import Callable
from inspect import signature, Parameter
from typing import Type, Optional

from sh_edraft.configuration.base.configuration_model_base import ConfigurationModelBase
from sh_edraft.database.context.base.database_context_base import DatabaseContextBase
from sh_edraft.environment.base import EnvironmentBase
from sh_edraft.hosting.base.application_runtime_base import ApplicationRuntimeBase
from sh_edraft.service.providing.base.service_provider_base import ServiceProviderBase
from sh_edraft.service.base.service_base import ServiceBase


class ServiceProvider(ServiceProviderBase):

    def __init__(self, app_runtime: ApplicationRuntimeBase):
        ServiceProviderBase.__init__(self)
        self._app_runtime: ApplicationRuntimeBase = app_runtime
        self._database_context: Optional[DatabaseContextBase] = None

        self._transient_services: dict[Type[ServiceBase], Type[ServiceBase]] = {}
        self._scoped_services: dict[Type[ServiceBase], Type[ServiceBase]] = {}
        self._singleton_services: dict[Type[ServiceBase], ServiceBase] = {}

    def create(self): pass

    def _create_instance(self, service: Callable[ServiceBase]) -> ServiceBase:
        sig = signature(service.__init__)
        params = []
        for param in sig.parameters.items():
            parameter = param[1]
            if parameter.name != 'self' and parameter.annotation != Parameter.empty:
                if issubclass(parameter.annotation, ApplicationRuntimeBase):
                    params.append(self._app_runtime)

                elif issubclass(parameter.annotation, EnvironmentBase):
                    params.append(self._app_runtime.configuration.environment)

                elif issubclass(parameter.annotation, DatabaseContextBase):
                    params.append(self._database_context)

                elif issubclass(parameter.annotation, ServiceBase):
                    params.append(self.get_service(parameter.annotation))

                elif issubclass(parameter.annotation, ConfigurationModelBase):
                    params.append(self._app_runtime.configuration.get_configuration(parameter.annotation))

        return service(*params)

    def add_db_context(self, db_context: Type[DatabaseContextBase]):
        self._database_context = self._create_instance(db_context)

    def get_db_context(self) -> Callable[DatabaseContextBase]:
        return self._database_context

    def add_transient(self, service_type: Type[ServiceBase], service: Type[ServiceBase]):
        self._transient_services[service_type] = service

    def add_scoped(self, service_type: Type[ServiceBase], service: Type[ServiceBase]):
        self._scoped_services[service_type] = service

    def add_singleton(self, service_type: Type[ServiceBase], service: Callable[ServiceBase]):
        for known_service in self._singleton_services:
            if type(known_service) == service_type:
                raise Exception(f'Service with type {service_type} already exists')

        self._singleton_services[service_type] = self._create_instance(service)

    def get_service(self, instance_type: Type[ServiceBase]) -> Callable[ServiceBase]:
        for service in self._transient_services:
            if service == instance_type and isinstance(self._transient_services[service], type(instance_type)):
                return self._create_instance(self._transient_services[service])

        for service in self._scoped_services:
            if service == instance_type and isinstance(self._scoped_services[service], type(instance_type)):
                return self._create_instance(self._scoped_services[service])

        for service in self._singleton_services:
            if service == instance_type and isinstance(self._singleton_services[service], instance_type):
                return self._singleton_services[service]

    def remove_service(self, instance_type: Type[ServiceBase]):
        for service in self._transient_services:
            if service == instance_type and isinstance(self._transient_services[service], type(instance_type)):
                del self._transient_services[service]
                return

        for service in self._scoped_services:
            if service == instance_type and isinstance(self._scoped_services[service], type(instance_type)):
                del self._scoped_services[service]
                return

        for service in self._singleton_services:
            if service == instance_type and isinstance(self._singleton_services[service], instance_type):
                del self._singleton_services[service]
                return
