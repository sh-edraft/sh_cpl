from abc import abstractmethod, ABC
from collections import Callable
from typing import Type

from cpl.dependency_injection.service_abc import ServiceABC


class ServiceProviderABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC for service providing
        """
        pass

    @abstractmethod
    def build_service(self, service_type: type) -> object: pass

    @abstractmethod
    def get_service(self, instance_type: Type) -> Callable[ServiceABC]:
        """
        Returns instance of given type
        :param instance_type:
        :return:
        """
        pass
