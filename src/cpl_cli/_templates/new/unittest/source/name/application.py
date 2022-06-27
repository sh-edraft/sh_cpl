import textwrap

from cpl_cli._templates.template_file_abc import TemplateFileABC


class ApplicationTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str, use_async: bool):
        TemplateFileABC.__init__(self)

        self._name = 'application.py'
        self._path = path
        self._use_async = use_async
        
        if self._use_async:
            self._value = textwrap.dedent("""\
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
            """)
        else:
            self._value = textwrap.dedent("""\
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
