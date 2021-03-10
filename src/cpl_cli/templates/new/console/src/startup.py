import textwrap

from cpl_cli.templates.template_file_abc import TemplateFileABC


class StartupTemplate(TemplateFileABC):

    def __init__(self):
        TemplateFileABC.__init__(self)

        self._name = 'startup.py'
        self._path = 'src/'
        self._value = textwrap.dedent("""\
            from typing import Optional

            from cpl.application.application_host import ApplicationHost
            from cpl.application.application_host_abc import ApplicationHostABC
            from cpl.application.startup_abc import StartupABC
            from cpl.configuration.configuration_abc import ConfigurationABC
            from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
            
            
            class Startup(StartupABC):
            
                def __init__(self):
                    StartupABC.__init__(self)
            
                    self._app_host: Optional[ApplicationHostABC] = None
                    self._configuration: Optional[ConfigurationABC] = None
                    self._services: Optional[ServiceProviderABC] = None
            
                def create_application_host(self) -> ApplicationHostABC:
                    self._app_host = ApplicationHost()
                    self._configuration = self._app_host.configuration
                    self._services = self._app_host.services
                    return self._app_host
            
                def create_configuration(self) -> ConfigurationABC:
                    pass
            
                    return self._configuration
            
                def create_services(self) -> ServiceProviderABC:
                    pass
            
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
