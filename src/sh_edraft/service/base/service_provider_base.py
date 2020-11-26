from abc import abstractmethod
from collections import Callable
from typing import Type

from sh_edraft.service.base.service_base import ServiceBase


class ServiceProviderBase(ServiceBase):

    @abstractmethod
    def __init__(self):
        ServiceBase.__init__(self)

    @abstractmethod
    def add_transient(self, service_type: Type[ServiceBase], service: Type[ServiceBase]): pass

    @abstractmethod
    def add_scoped(self, service_type: Type[ServiceBase], service: Type[ServiceBase]): pass

    @abstractmethod
    def add_singleton(self, service_type: Type[ServiceBase], service: ServiceBase): pass

    @abstractmethod
    def get_service(self, instance_type: Type[ServiceBase]) -> Callable[ServiceBase]: pass

    @abstractmethod
    def remove_service(self, instance_type: type): pass
