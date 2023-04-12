from cpl_core.configuration import ConfigurationABC
from cpl_core.dependency_injection import ServiceProvider, ServiceProviderABC
from di.test_service import TestService


class StaticTest:
    @staticmethod
    @ServiceProvider.inject
    def test(services: ServiceProviderABC, config: ConfigurationABC, t1: TestService):
        t1.run()
