import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Application(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        from cpl_core.application import ApplicationABC
        from cpl_core.configuration import ConfigurationABC
        from cpl_core.console import Console
        from cpl_core.dependency_injection import ServiceProviderABC
                    
                    
        class $Name(ApplicationABC):
                
            def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
                ApplicationABC.__init__(self, config, services)
                
            def configure(self):
                pass
                
            def main(self):
                Console.write_line('Hello World')
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'application',
            ['app', 'APP']
        )
