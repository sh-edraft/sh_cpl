from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Custom(GenerateSchematicABC):
    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        class $Name:

            def __init__(self):
                print('hello')
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(cls, "custom", ["cm", "CM"])
