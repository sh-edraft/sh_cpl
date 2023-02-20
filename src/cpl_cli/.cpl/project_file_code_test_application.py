from cpl_cli.abc.code_file_template_abc import CodeFileTemplateABC


class ProjectFileTestApplication(CodeFileTemplateABC):
    def __init__(
        self, path: str, use_application_api: bool, use_startup: bool, use_service_providing: bool, use_async: bool
    ):
        CodeFileTemplateABC.__init__(
            self, "application", path, "", use_application_api, use_startup, use_service_providing, use_async
        )

    def get_code(self) -> str:
        import textwrap

        if self._use_async:
            return textwrap.dedent(
                """\
            import unittest
            from unittest import TestSuite
            
            from cpl_core.application import ApplicationABC
            from cpl_core.configuration import ConfigurationABC
            from cpl_core.dependency_injection import ServiceProviderABC
            from unittests.test_case import TestCase
                
                
            class Application(ApplicationABC):
            
                def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
                    ApplicationABC.__init__(self, config, services)
                    self._suite: TestSuite = unittest.TestSuite()
            
                async def configure(self):
                    self._suite.addTest(TestCase('test_equal'))
            
                async def main(self):
                    runner = unittest.TextTestRunner()
                    runner.run(self._suite)
            """
            )

        return textwrap.dedent(
            """\
        import unittest
        from unittest import TestSuite
        
        from cpl_core.application import ApplicationABC
        from cpl_core.configuration import ConfigurationABC
        from cpl_core.dependency_injection import ServiceProviderABC
        from unittests.test_case import TestCase
            
            
        class Application(ApplicationABC):
        
            def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
                ApplicationABC.__init__(self, config, services)
                self._suite: TestSuite = unittest.TestSuite()
        
            def configure(self):
                self._suite.addTest(TestCase('test_equal'))
        
            def main(self):
                runner = unittest.TextTestRunner()
                runner.run(self._suite)
        """
        )
