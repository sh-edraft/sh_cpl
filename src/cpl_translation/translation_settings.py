import traceback

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.console import Console


class TranslationSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self._languages = []
        self._default_lang = ''

    @property
    def languages(self) -> list[str]:
        return self._languages

    @property
    def default_language(self) -> str:
        return self._default_lang

    def from_dict(self, settings: dict):
        try:
            self._languages = settings['Languages']
            self._default_lang = settings['DefaultLanguage']
        except Exception as e:
            Console.error(f'[ ERROR ] [ {__name__} ]: Reading error in {type(self).__name__} settings')
            Console.error(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
