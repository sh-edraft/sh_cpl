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
        
            def __init__(self):
                ConfigurationModelABC.__init__(self)
        
                self._atr = ''
        
            @property
            def atr(self) -> str:
                return self._atr
        
            def from_dict(self, settings: dict):
                try:
                    self._atr = settings['atr']
                except Exception as e:
                    Console.error(f'[ ERROR ] [ {__name__} ]: Reading error in {type(self).__name__} settings')
                    Console.error(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'settings',
            ['st', 'ST']
        )
