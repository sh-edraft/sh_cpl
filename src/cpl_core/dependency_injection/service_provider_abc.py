from abc import abstractmethod, ABC
from collections import Callable
from typing import Type, Optional

from cpl_core.dependency_injection.scope_abc import ScopeABC


class ServiceProviderABC(ABC):
    r"""ABC for the class :class:`cpl_core.dependency_injection.service_provider.ServiceProvider`"""

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
    def set_scope(self, scope: ScopeABC):
        r"""Sets the scope of service provider

        Parameter
        ---------
            scope :class:`cpl_core.dependency_injection.scope.Scope`
                Service scope
        """
        pass
    
    @abstractmethod
    def create_scope(self) -> ScopeABC:
        r"""Creates a service scope

        Returns
        -------
            Object of type :class:`cpl_core.dependency_injection.scope.Scope`
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
