import textwrap

from cpl_cli._templates.template_file_abc import TemplateFileABC


class TestCaseTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str, use_async: bool):
        TemplateFileABC.__init__(self)

        self._name = 'test_case.py'
        self._path = path
        self._use_async = use_async
        
        if self._use_async:
            self._value = textwrap.dedent("""\
                import unittest


                class TestCase(unittest.TestCase):
                
                    async def setUp(self) -> None:
                        pass
                
                    async def test_equal(self):
                        self.assertEqual(True, True)
            """)
        else:
            self._value = textwrap.dedent("""\
                import unittest


                class TestCase(unittest.TestCase):
                
                    def setUp(self) -> None:
                        pass
                
                    def test_equal(self):
                        self.assertEqual(True, True)
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
