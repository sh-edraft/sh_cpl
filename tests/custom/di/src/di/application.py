from cpl_core.application import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from cpl_core.dependency_injection.scope import Scope
from test_service_service import TestService
from di_tester_service import DITesterService


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
            Console.write_line('Scope1')
            ts: TestService = scope.service_provider.get_service(TestService)
            ts.run()
            dit: DITesterService = scope.service_provider.get_service(DITesterService)
            dit.run()
        
        #Console.write_line('Disposed:')
        #ts1: TestService = scope1.service_provider.get_service(TestService)
        #ts1.run()

        with self._services.create_scope() as scope:
            Console.write_line('Scope2')
            ts: TestService = scope.service_provider.get_service(TestService)
            ts.run()
            dit: DITesterService = scope.service_provider.get_service(DITesterService)
            dit.run()
        
        Console.write_line('Global')
        self._part_of_scoped()
