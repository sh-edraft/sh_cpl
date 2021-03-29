from abc import abstractmethod, ABC
from collections import Callable
from typing import Type, Optional


class ServiceProviderABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC for service providing
        """
        pass

    @abstractmethod
    def build_service(self, service_type: type) -> object:
        """
        Creates instance of given type
        :param service_type:
        :return:
        """
        pass

    @abstractmethod
    def get_service(self, instance_type: Type) -> Optional[Callable[object]]:
        """
        Returns instance of given type
        :param instance_type:
        :return:
        """
        pass
