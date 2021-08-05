from abc import abstractmethod, ABC
from collections import Callable
from typing import Type, Optional


class ServiceProviderABC(ABC):
    r"""ABC for the class :class:`cpl.dependency_injection.service_provider.ServiceProvider`"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def build_service(self, service_type: Type) -> object:
        r"""Creates instance of given type

        Parameter
        ---------
            instance_type: :class:`Type`
                The type of the searched instance

        Returns
        -------
            Object of the given type
        """
        pass

    @abstractmethod
    def get_service(self, instance_type: Type) -> Optional[Callable[object]]:
        r"""Returns instance of given type

        Parameter
        ---------
            instance_type: :class:`Type`
                The type of the searched instance

        Returns
        -------
            Object of type Optional[Callable[:class:`object`]]
        """
        pass
