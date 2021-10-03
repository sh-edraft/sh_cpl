import textwrap

from cpl_cli._templates.template_file_abc import TemplateFileABC


class ApplicationTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str):
        TemplateFileABC.__init__(self)

        self._name = 'application.py'
        self._path = path
        self._value = textwrap.dedent("""\
            from cpl_core.application import ApplicationABC
            from cpl_core.configuration import ConfigurationABC
            from cpl_core.console import Console
            from cpl_core.dependency_injection import ServiceProviderABC
                
                
            class Application(ApplicationABC):
            
                def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
                    ApplicationABC.__init__(self, config, services)
            
                def configure(self):
                    pass
            
                def main(self):
                    Console.write_line('Hello World')
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
