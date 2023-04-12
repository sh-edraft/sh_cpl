from cpl_cli.abc.code_file_template_abc import CodeFileTemplateABC


class ProjectFileTestCase(CodeFileTemplateABC):
    def __init__(
        self, path: str, use_application_api: bool, use_startup: bool, use_service_providing: bool, use_async: bool
    ):
        CodeFileTemplateABC.__init__(
            self, "test_case", path, "", use_application_api, use_startup, use_service_providing, use_async
        )

    def get_code(self) -> str:
        import textwrap

        if self._use_async:
            return textwrap.dedent(
                """\
            import unittest


            class TestCase(unittest.TestCase):
                
                async def setUp(self) -> None:
                    pass
                
                async def test_equal(self):
                    self.assertEqual(True, True)
            """
            )

        return textwrap.dedent(
            """\
        import unittest


            class TestCase(unittest.TestCase):
                
                def setUp(self) -> None:
                    pass
                
                def test_equal(self):
                    self.assertEqual(True, True)
        """
        )
