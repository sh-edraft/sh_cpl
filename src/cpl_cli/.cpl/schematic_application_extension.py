import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class ApplicationExtension(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        from cpl_core.application import ApplicationExtensionABC
        from cpl_core.configuration import ConfigurationABC
        from cpl_core.dependency_injection import ServiceProviderABC
        
        
        class $Name(ApplicationExtensionABC):
        
            def __init__(self):
                ApplicationExtensionABC.__init__(self)
        
            def run(self, config: ConfigurationABC, services: ServiceProviderABC):
                pass
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'application-extension',
            ['appex', 'APPEX']
        )
