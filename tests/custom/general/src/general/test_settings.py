from cpl_core.configuration import ConfigurationModelABC


class TestSettings(ConfigurationModelABC):
    def __init__(self, value: int = None):
        self.value = value
