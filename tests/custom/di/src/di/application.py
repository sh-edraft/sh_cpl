from cpl_core.application import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from cpl_core.dependency_injection.scope import Scope
from di.static_test import StaticTest
from di.test_abc import TestABC
from di.test_service import TestService
from di.di_tester_service import DITesterService
from di.tester import Tester


class Application(ApplicationABC):
    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

    def _part_of_scoped(self):
        ts: TestService = self._services.get_service(TestService)
        ts.run()

    def configure(self):
        pass

    def main(self):
        with self._services.create_scope() as scope:
            Console.write_line("Scope1")
            ts: TestService = scope.service_provider.get_service(TestService)
            ts.run()
            dit: DITesterService = scope.service_provider.get_service(DITesterService)
            dit.run()

        with self._services.create_scope() as scope:
            Console.write_line("Scope2")
            ts: TestService = scope.service_provider.get_service(TestService)
            ts.run()
            dit: DITesterService = scope.service_provider.get_service(DITesterService)
            dit.run()

        Console.write_line("Global")
        self._part_of_scoped()
        StaticTest.test()

        self._services.get_service(Tester)
        Console.write_line(self._services.get_services(list[TestABC]))
