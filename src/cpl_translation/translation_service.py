import json
import os.path
from functools import reduce

from cpl_translation.translation_service_abc import TranslationServiceABC
from cpl_translation.translation_settings import TranslationSettings


class TranslationService(TranslationServiceABC):

    def __init__(self):
        self._translation = {}

        self._language = ''
        self._default_language = ''

        TranslationServiceABC.__init__(self)

    def set_default_lang(self, lang: str):
        if lang not in self._translation:
            raise KeyError()

        self._default_language = lang
        self.set_lang(lang)

    def set_lang(self, lang: str):
        if lang not in self._translation:
            raise KeyError()

        self._language = lang

    def load(self, lang: str):
        if not os.path.exists(f'translation/{lang}.json'):
            raise FileNotFoundError()

        file_dict = {}
        with open(f'translation/{lang}.json', 'r', encoding='utf8') as file:
            file_dict = json.load(file)
            file.close()

        self._translation[lang] = file_dict

    def load_by_settings(self, settings: TranslationSettings):
        if settings is None:
            raise Exception(f'{TranslationSettings.__name__} not loaded')

        self._language = settings.default_language
        self._default_language = settings.default_language

        for lang in settings.languages:
            self.load(lang)

    def translate(self, key: str) -> str:
        value = reduce(lambda d, key: d.get(key) if isinstance(d, dict) else None, key.split("."), self._translation[self._language])

        if value is None:
            raise KeyError(f'Translation {key} not found')

        return value
