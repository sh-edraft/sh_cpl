import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class ConfigModel(GenerateSchematicABC):
    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        import traceback

        from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
        from cpl_core.console import Console
        
        
        class $Name(ConfigurationModelABC):
        
            def __init__(self, atr: str = None):
                ConfigurationModelABC.__init__(self)
        
                self._atr = atr
        
            @property
            def atr(self) -> str:
                return self._atr
        
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(cls, "settings", ["st", "ST"])
