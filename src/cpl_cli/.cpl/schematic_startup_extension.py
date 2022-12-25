import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class StartupExtension(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        from cpl_core.application.startup_extension_abc import StartupExtensionABC
        from cpl_core.configuration.configuration_abc import ConfigurationABC
        from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
        from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
        
        
        class $Name(StartupExtensionABC):
        
            def __init__(self):
                pass
        
            def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
                pass
        
            def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC):
                pass
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'startup-extension',
            ['stupex', 'STUPEX']
        )
