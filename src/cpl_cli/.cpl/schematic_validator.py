import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Validator(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        from cpl_core.configuration.validator_abc import ValidatorABC
        
        
        class $Name(ValidatorABC):
        
            def __init__(self):
                ValidatorABC.__init__(self)
        
            def validate(self) -> bool:
                return True
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'validator',
            ['v', 'V']
        )
