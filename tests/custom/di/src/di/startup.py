from cpl_core.application import StartupABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.dependency_injection import ServiceProviderABC, ServiceCollectionABC
from cpl_core.environment import ApplicationEnvironment
from di.test1_service import Test1Service
from di.test2_service import Test2Service
from di.test_abc import TestABC
from di.test_service import TestService
from di.di_tester_service import DITesterService
from di.tester import Tester


class Startup(StartupABC):
    def __init__(self):
        StartupABC.__init__(self)

    def configure_configuration(
        self, configuration: ConfigurationABC, environment: ApplicationEnvironment
    ) -> ConfigurationABC:
        return configuration

    def configure_services(
        self, services: ServiceCollectionABC, environment: ApplicationEnvironment
    ) -> ServiceProviderABC:
        services.add_scoped(TestService)
        services.add_scoped(DITesterService)

        services.add_singleton(TestABC, Test1Service)
        services.add_singleton(TestABC, Test2Service)
        services.add_singleton(Tester)

        return services.build_service_provider()
