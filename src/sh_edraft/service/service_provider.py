from collections import Callable
from typing import Type

from termcolor import colored

from sh_edraft.service.base.service_provider_base import ServiceProviderBase
from sh_edraft.service.base.service_base import ServiceBase
from sh_edraft.service.model.provide_state import ProvideState


class ServiceProvider(ServiceProviderBase):

    def __init__(self):
        super().__init__()

    def init(self, args: tuple): pass

    def create(self): pass

    @staticmethod
    def _create_instance(service: type[ServiceBase], args: tuple) -> ServiceBase:
        instance = service()
        try:
            instance.init(args)
            return instance
        except Exception as e:
            print(colored(f'Argument error\n{e}', 'red'))

    def add_transient(self, service: Type[ServiceBase], *args):
        self._transient_services.append(ProvideState(service, args))

    def add_scoped(self, service: Type[ServiceBase], *args):
        self._transient_services.append(ProvideState(service, args))

    def add_singleton(self, service: Type[ServiceBase], *args):
        for known_service in self._singleton_services:
            if type(known_service) == type(service):
                raise Exception(f'Service from type {type(service)} already exists')

        self._singleton_services.append(self._create_instance(service, args))

    def get_service(self, instance_type: Type[ServiceBase]) -> Callable[ServiceBase]:
        for state in self._transient_services:
            if isinstance(state.service, type(instance_type)):
                return self._create_instance(state.service, state.args)

        for state in self._scoped_services:
            if isinstance(state.service, type(instance_type)):
                return self._create_instance(state.service, state.args)

        for service in self._singleton_services:
            if isinstance(service, instance_type):
                return service

    def remove_service(self, instance_type: type):
        for state in self._transient_services:
            if isinstance(state.service, type(instance_type)):
                self._transient_services.remove(state)
                return

        for state in self._scoped_services:
            if isinstance(state.service, type(instance_type)):
                self._scoped_services.remove(state)
                return

        for service in self._singleton_services:
            if isinstance(service, instance_type):
                self._singleton_services.remove(service)
                return
