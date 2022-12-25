from cpl_cli.abc.code_file_template_abc import CodeFileTemplateABC


class ProjectFileApplication(CodeFileTemplateABC):

    def __init__(self, path: str, use_application_api: bool, use_startup: bool, use_service_providing: bool, use_async: bool):
        CodeFileTemplateABC.__init__(self, 'application', path, '', use_application_api, use_startup, use_service_providing, use_async)

    def get_code(self) -> str:
        import textwrap

        if self._use_async:
            return textwrap.dedent("""\
            from cpl_core.application import ApplicationABC
            from cpl_core.configuration import ConfigurationABC
            from cpl_core.console import Console
            from cpl_core.dependency_injection import ServiceProviderABC
                    
                    
            class Application(ApplicationABC):
                
                def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
                    ApplicationABC.__init__(self, config, services)
                
                async def configure(self):
                    pass
                
                async def main(self):
                    Console.write_line('Hello World')
            """)

        return textwrap.dedent("""\
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
