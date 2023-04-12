from cpl_core.console import Console
from cpl_core.pipes.pipe_abc import PipeABC
from cpl_translation.translation_service_abc import TranslationServiceABC


class TranslatePipe(PipeABC):
    def __init__(self, translation: TranslationServiceABC):
        self._translation = translation

    def transform(self, value: any, *args):
        try:
            return self._translation.translate(value)
        except KeyError as e:
            Console.error(f"Translation {value} not found")
            return ""
