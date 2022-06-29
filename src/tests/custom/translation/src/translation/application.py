from cpl_core.application import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from cpl_translation.translate_pipe import TranslatePipe
from cpl_translation.translation_service_abc import TranslationServiceABC
from cpl_translation.translation_settings import TranslationSettings


class Application(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

        self._translate: TranslatePipe = services.get_service(TranslatePipe)
        self._translation: TranslationServiceABC = services.get_service(TranslationServiceABC)
        self._translation_settings: TranslationSettings = config.get_configuration(TranslationSettings)

        self._translation.load_by_settings(config.get_configuration(TranslationSettings))
        self._translation.set_default_lang('de')

    def configure(self):
        pass

    def main(self):
        Console.write_line(self._translate.transform('main.text.hello_world'))
        self._translation.set_lang('en')
        Console.write_line(self._translate.transform('main.text.hello_world'))
        Console.write_line(self._translate.transform('main.text.hello'))
