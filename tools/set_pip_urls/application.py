import json
import os
import sys
from typing import Optional

from cpl_core.environment import EnvironmentNameEnum

from cpl_core.application import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from set_pip_urls.pip_settings import PIPSettings


class Application(ApplicationABC):
    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

        self._pip_settings: Optional[PIPSettings] = config.get_configuration(PIPSettings)

    def configure(self):
        self._configuration.parse_console_arguments(self._services)

    def main(self):
        if self._pip_settings is None:
            Console.error("appsettings.json not found")
            sys.exit()

        url = None
        match self._environment.environment_name:
            case EnvironmentNameEnum.production.value:
                url = self._pip_settings.production
            case EnvironmentNameEnum.staging.value:
                url = self._pip_settings.staging
            case EnvironmentNameEnum.development.value:
                url = self._pip_settings.development

        cli_json = {"CLI": {"PipPath": url}}
        file = os.path.abspath(
            os.path.join(self._environment.working_directory, "../../src/cpl_cli", "appsettings.json")
        )
        Console.write_line(f"Writing PipPath: {url} to {file}")
        with open(file, "w") as f:
            f.write(json.dumps(cli_json, indent=2))
            f.close()
