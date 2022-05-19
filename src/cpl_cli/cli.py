import sys
import traceback

from cpl_core.application.application_abc import ApplicationABC
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.dependency_injection import ServiceProviderABC


class CLI(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        """
        CPL CLI
        """
        ApplicationABC.__init__(self, config, services)

        self._options: list[str] = []

    def configure(self):
        pass

    def main(self):
        """
        Entry point of the CPL CLI
        :return:
        """
        try:
            self._configuration.parse_console_arguments()
        except KeyboardInterrupt:
            Console.write_line()
            sys.exit()
        except Exception as e:
            Console.error(str(e), traceback.format_exc())
            sys.exit()
