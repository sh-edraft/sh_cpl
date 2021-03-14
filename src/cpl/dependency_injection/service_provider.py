from collections import Callable
from inspect import signature, Parameter
from typing import Type, Optional, Union

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.database.context.database_context_abc import DatabaseContextABC
from cpl.dependency_injection.service_abc import ServiceABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl.environment.environment_abc import ApplicationEnvironmentABC


class ServiceProvider(ServiceProviderABC):

    def __init__(self, app_runtime: ApplicationRuntimeABC):
        ServiceProviderABC.__init__(self)
        self._app_runtime: ApplicationRuntimeABC = app_runtime
        self._database_context: Optional[DatabaseContextABC] = None

        self._transient_services: dict[Type[ServiceABC], Callable[ServiceABC]] = {}
        self._scoped_services: dict[Type[ServiceABC], Callable[ServiceABC]] = {}
        self._singleton_services: dict[Type[ServiceABC], Callable[ServiceABC], ServiceABC] = {}

    def _create_instance(self, service: Union[Callable[ServiceABC], ServiceABC]) -> Callable[ServiceABC]:
        sig = signature(service.__init__)
        params = []
        for param in sig.parameters.items():
            parameter = param[1]
            if parameter.name != 'self' and parameter.annotation != Parameter.empty:
                if issubclass(parameter.annotation, ApplicationRuntimeABC):
                    params.append(self._app_runtime)

                elif issubclass(parameter.annotation, ApplicationEnvironmentABC):
                    params.append(self._app_runtime.configuration.environment)

                elif issubclass(parameter.annotation, DatabaseContextABC):
                    params.append(self._database_context)

                elif issubclass(parameter.annotation, ConfigurationModelABC):
                    params.append(self._app_runtime.configuration.get_configuration(parameter.annotation))

                elif issubclass(parameter.annotation, ConfigurationABC):
                    params.append(self._app_runtime.configuration)

                elif issubclass(parameter.annotation, ServiceProviderABC):
                    params.append(self)

                else:
                    params.append(self.get_service(parameter.annotation))

        return service(*params)

    def add_db_context(self, db_context: Type[DatabaseContextABC]):
        self._database_context = self._create_instance(db_context)

    def get_db_context(self) -> Callable[DatabaseContextABC]:
        return self._database_context

    def add_transient(self, service_type: Type[ServiceABC], service: Callable[ServiceABC] = None):
        if service is None:
            self._transient_services[service_type] = service_type
        else:
            self._transient_services[service_type] = service

    def add_scoped(self, service_type: Type[ServiceABC], service: Callable[ServiceABC] = None):
        if service is None:
            self._scoped_services[service_type] = service_type
        else:
            self._scoped_services[service_type] = service

    def add_singleton(self, service_type: Type[ServiceABC], service: Callable[ServiceABC] = None):
        for known_service in self._singleton_services:
            if type(known_service) == service_type:
                raise Exception(f'Service with type {service_type} already exists')

        if service is None:
            self._singleton_services[service_type] = self._create_instance(service_type)
        else:
            self._singleton_services[service_type] = self._create_instance(service)

    def get_service(self, instance_type: Type) -> Callable[ServiceABC]:
        if issubclass(instance_type, ServiceProviderABC):
            return self

        for service in self._transient_services:
            if service == instance_type and isinstance(self._transient_services[service], type(instance_type)):
                return self._create_instance(self._transient_services[service])

        for service in self._scoped_services:
            if service == instance_type and isinstance(self._scoped_services[service], type(instance_type)):
                return self._create_instance(self._scoped_services[service])

        for service in self._singleton_services:
            if service == instance_type and isinstance(self._singleton_services[service], instance_type):
                return self._singleton_services[service]

    def remove_service(self, instance_type: Type[ServiceABC]):
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
