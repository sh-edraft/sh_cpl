from cpl_cli.abc.code_file_template_abc import CodeFileTemplateABC


class ProjectFileStartup(CodeFileTemplateABC):

    def __init__(self, path: str, use_application_api: bool, use_startup: bool, use_service_providing: bool, use_async: bool):
        CodeFileTemplateABC.__init__(self, 'startup', path, '', use_application_api, use_startup, use_service_providing, use_async)

    def get_code(self) -> str:
        import textwrap

        return textwrap.dedent("""\
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
