import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC
from cpl_core.utils import String


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
        return self.build_code_str(code, Name=String.convert_to_camel_case(self._class_name))

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(cls, "test-case", ["tc", "TC"])
