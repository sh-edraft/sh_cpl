import os.path
import textwrap

from cpl.utils.string import String
from cpl_cli._templates.template_file_abc import TemplateFileABC


class ApplicationTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str):
        TemplateFileABC.__init__(self)

        name = String.convert_to_snake_case(name)
        self._name = 'application.py'
        self._path = os.path.join(path, name)
        self._value = textwrap.dedent("""\
            from cpl.application import ApplicationABC
            from cpl.configuration import ConfigurationABC
            from cpl.console import Console
            from cpl.dependency_injection import ServiceProviderABC
                
                
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
