from abc import ABC, abstractmethod
from collections import Callable
from typing import Type

from sh_edraft.service.base.service_base import ServiceBase
from sh_edraft.service.model.provide_state import ProvideState


class ProviderBase(ABC):

    @abstractmethod
    def __init__(self):
        self._transient_services: list[ProvideState] = []
        self._scoped_services: list[ProvideState] = []
        self._singleton_services: list[ServiceBase] = []

    @abstractmethod
    def add_transient(self, service: Type[ServiceBase], *args): pass

    @abstractmethod
    def add_scoped(self, service: Type[ServiceBase], *args): pass

    @abstractmethod
    def add_singleton(self, service: Type[ServiceBase], *args): pass

    @abstractmethod
    def get_service(self, instance_type: type) -> Callable[ServiceBase]: pass

    @abstractmethod
    def remove_service(self, instance_type: type): pass
