import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class TestCase(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        import unittest


        class $Name(unittest.TestCase):
        
            def setUp(self):
                pass
        
            def test_equal(self):
                pass
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'test-case',
            ['tc', 'TC']
        )
