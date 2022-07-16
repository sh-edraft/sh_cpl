from abc import ABC, abstractmethod

from cpl_translation import TranslationSettings


class TranslationServiceABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def set_default_lang(self, lang: str): pass

    @abstractmethod
    def set_lang(self, lang: str): pass

    @abstractmethod
    def load(self, lang: str): pass

    @abstractmethod
    def load_by_settings(self, settings: TranslationSettings): pass

    @abstractmethod
    def translate(self, key: str) -> str: pass
