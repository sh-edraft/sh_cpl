from collections import Callable
from inspect import signature, Parameter
from typing import Type

from sh_edraft.configuration.configuration import Configuration
from sh_edraft.hosting.base.application_host_base import ApplicationHostBase
from sh_edraft.configuration.base.configuration_model_base import ConfigurationModelBase
from sh_edraft.service.base.service_provider_base import ServiceProviderBase
from sh_edraft.service.base.service_base import ServiceBase


class ServiceProvider(ServiceProviderBase):

    def __init__(self):
        super().__init__()
        self._config = Configuration()

    @property
    def config(self):
        return self._config

    def create(self): pass

    def _create_instance(self, service: Callable[ServiceBase]) -> ServiceBase:
        sig = signature(service.__init__)
        params = []
        for param in sig.parameters.items():
            parameter = param[1]
            if parameter.name != 'self' and parameter.annotation != Parameter.empty:
                if issubclass(parameter.annotation, ServiceBase):
                    params.append(self.get_service(parameter.annotation))

                elif issubclass(parameter.annotation, ConfigurationModelBase) or issubclass(parameter.annotation, ApplicationHostBase):
                    params.append(self._config.get_config_by_type(parameter.annotation))

        return service(*params)
        # try:
        #    instance.init(args)
        #    return instance
        # except Exception as e:
        #    print(colored(f'Argument error\n{e}', 'red'))

    def add_transient(self, service_type: Type[ServiceBase], service: Type[ServiceBase]):
        self._transient_services[service_type] = service

    def add_scoped(self, service_type: Type[ServiceBase], service: Type[ServiceBase]):
        self._scoped_services[service_type] = service

    def add_singleton(self, service_type: Type[ServiceBase], service: ServiceBase):
        for known_service in self._singleton_services:
            if type(known_service) == type(service_type):
                raise Exception(f'Service with type {type(service_type)} already exists')

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
            if isinstance(service, type(instance_type)):
                del self._transient_services[service]
                return

        for service in self._scoped_services:
            if isinstance(service, type(instance_type)):
                del self._scoped_services[service]
                return

        for service in self._singleton_services:
            if isinstance(service, instance_type):
                del self._singleton_services[service]
                return
