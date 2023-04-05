import os
import unittest
from typing import Optional

from cpl_translation import TranslationService, TranslatePipe, TranslationSettings
from unittests_cli.constants import TRANSLATION_PATH


class TranslationTestCase(unittest.TestCase):
    def __init__(self, methodName: str):
        unittest.TestCase.__init__(self, methodName)
        self._translation: Optional[TranslationService] = None
        self._translate: Optional[TranslatePipe] = None

    def setUp(self):
        os.chdir(os.path.abspath(TRANSLATION_PATH))
        self._translation = TranslationService()
        settings = TranslationSettings(["de", "en"], "en")
        self._translation.load_by_settings(settings)
        self._translation.set_default_lang("de")
        self._translate = TranslatePipe(self._translation)

    def cleanUp(self):
        pass

    def test_service(self):
        self.assertEqual("Hallo Welt", self._translation.translate("main.text.hello_world"))
        self._translation.set_lang("en")
        self.assertEqual("Hello World", self._translation.translate("main.text.hello_world"))
        with self.assertRaises(KeyError) as ctx:
            self._translation.translate("main.text.hallo_welt")

        self.assertTrue(type(ctx.exception) == KeyError)
        self.assertIn("Translation main.text.hallo_welt not found", str(ctx.exception))

        with self.assertRaises(FileNotFoundError) as ctx:
            self._translation.load("DE")

        self.assertTrue(type(ctx.exception) == FileNotFoundError)

        with self.assertRaises(KeyError) as ctx:
            self._translation.set_lang("DE")

        self.assertTrue(type(ctx.exception) == KeyError)

        with self.assertRaises(KeyError) as ctx:
            self._translation.set_default_lang("DE")

        self.assertTrue(type(ctx.exception) == KeyError)

    def test_pipe(self):
        self.assertEqual("Hallo Welt", self._translate.transform("main.text.hello_world"))
        self._translation.set_lang("en")
        self.assertEqual("Hello World", self._translate.transform("main.text.hello_world"))
        with self.assertRaises(KeyError) as ctx:
            self._translation.translate("main.text.hallo_welt")

        self.assertTrue(type(ctx.exception) == KeyError)
        self.assertIn("Translation main.text.hallo_welt not found", str(ctx.exception))
