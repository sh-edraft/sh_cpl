
from cpl_core.console.console import Console
from cpl_core.dependency_injection.scope_abc import ScopeABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC


class Scope(ScopeABC):

    def __init__(self, service_provider: ServiceProviderABC):
        self._service_provider = service_provider
        self._service_provider.set_scope(self)

    @property
    def service_provider(self) -> ServiceProviderABC:
        return self._service_provider
    
    def dispose(self):
        self._service_provider = None
