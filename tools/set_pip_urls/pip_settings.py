from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC


class PIPSettings(ConfigurationModelABC):
    def __init__(self, production: str = None, staging: str = None, development: str = None):
        ConfigurationModelABC.__init__(self)

        self._production = production
        self._staging = staging
        self._development = development

    @property
    def production(self):
        return self._production

    @property
    def staging(self):
        return self._staging

    @property
    def development(self):
        return self._development
