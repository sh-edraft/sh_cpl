import functools
from abc import abstractmethod, ABC
from inspect import Signature, signature
from typing import Type, Optional

from cpl_core.dependency_injection.scope_abc import ScopeABC
from cpl_core.type import T


class ServiceProviderABC(ABC):
    r"""ABC for the class :class:`cpl_core.dependency_injection.service_provider.ServiceProvider`"""

    _provider: Optional['ServiceProviderABC'] = None

    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def set_global_provider(cls, provider: 'ServiceProviderABC'):
        cls._provider = provider

    @abstractmethod
    def build_by_signature(self, sig: Signature) -> list[T]:
        pass

    @abstractmethod
    def build_service(self, service_type: type) -> object:
        r"""Creates instance of given type

        Parameter
        ---------
            instance_type: :class:`type`
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
            Object of type :class:`cpl_core.dependency_injection.scope_abc.ScopeABC`
                Service scope
        """
        pass

    @abstractmethod
    def create_scope(self) -> ScopeABC:
        r"""Creates a service scope

        Returns
        -------
            Object of type :class:`cpl_core.dependency_injection.scope_abc.ScopeABC`
        """
        pass

    @abstractmethod
    def get_service(self, instance_type: T) -> Optional[T]:
        r"""Returns instance of given type

        Parameter
        ---------
            instance_type: :class:`cpl_core.type.T`
                The type of the searched instance

        Returns
        -------
            Object of type Optional[:class:`cpl_core.type.T`]
        """
        pass

    @abstractmethod
    def get_services(self, service_type: T) -> list[Optional[T]]:
        r"""Returns instance of given type

        Parameter
        ---------
            instance_type: :class:`cpl_core.type.T`
                The type of the searched instance

        Returns
        -------
            Object of type list[Optional[:class:`cpl_core.type.T`]
        """
        pass

    @classmethod
    def inject(cls, f=None):
        r"""Decorator to allow injection into static and class methods

        Parameter
        ---------
            f: Callable

        Returns
        -------
            function
        """
        if f is None:
            return functools.partial(cls.inject)

        @functools.wraps(f)
        def inner(*args, **kwargs):
            if cls._provider is None:
                raise Exception(f'{cls.__name__} not build!')

            injection = [x for x in cls._provider.build_by_signature(signature(f)) if x is not None]
            return f(*injection, *args, **kwargs)

        return inner
