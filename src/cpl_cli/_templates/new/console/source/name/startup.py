import os.path
import textwrap

from cpl.utils.string import String
from cpl_cli._templates.template_file_abc import TemplateFileABC


class StartupTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str):
        TemplateFileABC.__init__(self)

        name = String.convert_to_snake_case(name)
        self._name = 'startup.py'
        self._path = os.path.join(path, name)
        self._value = textwrap.dedent("""\
            from cpl.application import StartupABC
            from cpl.configuration import ConfigurationABC
            from cpl.dependency_injection import ServiceProviderABC, ServiceCollectionABC
            
            
            class Startup(StartupABC):
            
                def __init__(self, config: ConfigurationABC, services: ServiceCollectionABC):
                    StartupABC.__init__(self)
            
                    self._configuration = config
                    self._environment = self._configuration.environment
                    self._services = services
            
                def configure_configuration(self) -> ConfigurationABC:
                    return self._configuration
            
                def configure_services(self) -> ServiceProviderABC:
                    return self._services.build_service_provider()
        """)

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    @property
    def value(self) -> str:
        return self._value
