from abc import ABC, abstractmethod

class ScopeABC(ABC):
    r"""ABC for the class :class:`cpl_core.dependency_injection.scope.Scope`"""
    
    def __init__(self):
        pass
    
    @property
    @abstractmethod
    def service_provider(self):
        r"""Returns to service provider of scope

        Returns
        -------
            Object of type :class:`cpl_core.dependency_injection.service_provider_abc.ServiceProviderABC`
        """
        pass
    
    @abstractmethod
    def dispose(self):
        r"""Sets service_provider to None
        """
        pass