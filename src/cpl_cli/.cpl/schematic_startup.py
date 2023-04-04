import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Startup(GenerateSchematicABC):
    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        from cpl_core.application import StartupABC
        from cpl_core.configuration import ConfigurationABC
        from cpl_core.dependency_injection import ServiceProviderABC, ServiceCollectionABC
        from cpl_core.environment import ApplicationEnvironment
        
        
        class $Name(StartupABC):
        
            def __init__(self):
                StartupABC.__init__(self)
        
            def configure_configuration(self, configuration: ConfigurationABC, environment: ApplicationEnvironment) -> ConfigurationABC:
                return configuration
        
            def configure_services(self, services: ServiceCollectionABC, environment: ApplicationEnvironment) -> ServiceProviderABC:
                return services.build_service_provider()
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(cls, "startup", ["stup", "STUP"])
