from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC


class TranslationSettings(ConfigurationModelABC):
    def __init__(
        self,
        languages: str = None,
        default_lang: str = None,
    ):
        ConfigurationModelABC.__init__(self)

        self._languages = [] if languages is None else languages
        self._default_lang = default_lang

    @property
    def languages(self) -> list[str]:
        return self._languages

    @property
    def default_language(self) -> str:
        return self._default_lang
