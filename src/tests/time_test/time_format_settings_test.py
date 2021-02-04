import unittest

from sh_edraft.time.model import TimeFormatSettingsNames, TimeFormatSettings


class TimeFormatSettingsTest(unittest.TestCase):

    def setUp(self): pass

    def test_from_dict(self):
        test_dict = {
            TimeFormatSettingsNames.date_format.value: '%H:%M:%S',
            TimeFormatSettingsNames.time_format.value: '%Y-%m-%d',
            TimeFormatSettingsNames.date_time_format.value: '%Y-%m-%d %H:%M:%S.%f',
            TimeFormatSettingsNames.date_time_log_format.value: '%Y-%m-%d_%H-%M-%S'
        }

        settings = TimeFormatSettings()
        settings.from_dict(test_dict)

        self.assertIsNotNone(settings)

        self.assertEqual(test_dict[TimeFormatSettingsNames.date_format.value], settings.date_format)
        self.assertEqual(test_dict[TimeFormatSettingsNames.time_format.value], settings.time_format)
        self.assertEqual(test_dict[TimeFormatSettingsNames.date_time_format.value], settings.date_time_format)
        self.assertEqual(test_dict[TimeFormatSettingsNames.date_time_log_format.value], settings.date_time_log_format)
