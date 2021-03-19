import textwrap

from cpl_cli.templates.template_file_abc import TemplateFileABC


class StartupTemplate(TemplateFileABC):

    def __init__(self):
        TemplateFileABC.__init__(self)

        self._name = 'startup.py'
        self._path = 'src/'
        self._value = textwrap.dedent("""\
            from cpl.application.application_runtime_abc import ApplicationRuntimeABC
            from cpl.application.startup_abc import StartupABC
            from cpl.configuration.configuration_abc import ConfigurationABC
            from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
            
            
            class Startup(StartupABC):
            
                def __init__(self, config: ConfigurationABC, runtime: ApplicationRuntimeABC, services: ServiceProviderABC):
                    StartupABC.__init__(self, config, runtime, services)
            
                def configure_configuration(self) -> ConfigurationABC:
                    return self._configuration
            
                def configure_services(self) -> ServiceProviderABC:
                    return self._services

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
