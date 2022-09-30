import textwrap

from cpl_cli._templates.template_file_abc import TemplateFileABC


class StartupTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str):
        TemplateFileABC.__init__(self)

        self._name = 'startup.py'
        self._path = path
        self._value = textwrap.dedent("""\
            from cpl_core.application import StartupABC
            from cpl_core.configuration import ConfigurationABC
            from cpl_core.dependency_injection import ServiceProviderABC, ServiceCollectionABC
            from cpl_core.environment import ApplicationEnvironment
            
            
            class Startup(StartupABC):
            
                def __init__(self):
                    StartupABC.__init__(self)
            
                def configure_configuration(self, configuration: ConfigurationABC, environment: ApplicationEnvironment) -> ConfigurationABC:
                    return configuration
            
                def configure_services(self, services: ServiceCollectionABC, environment: ApplicationEnvironment) -> ServiceProviderABC:
                    return services.build_service_provider()
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
