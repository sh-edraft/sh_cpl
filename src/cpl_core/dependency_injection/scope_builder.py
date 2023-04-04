from cpl_core.dependency_injection.scope import Scope
from cpl_core.dependency_injection.scope_abc import ScopeABC
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC


class ScopeBuilder:
    r"""Class to build :class:`cpl_core.dependency_injection.scope.Scope`"""

    def __init__(self, service_provider: ServiceProviderABC) -> None:
        self._service_provider = service_provider

    def build(self) -> ScopeABC:
        r"""Returns scope

        Returns:
            Object of type :class:`cpl_core.dependency_injection.scope.Scope`
        """
        return Scope(self._service_provider)
