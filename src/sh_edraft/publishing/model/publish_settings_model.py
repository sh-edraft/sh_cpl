import traceback
from typing import Optional

from sh_edraft.configuration.base.configuration_model_base import ConfigurationModelBase
from sh_edraft.publishing.model import Template
from sh_edraft.publishing.model.publish_settings_name import PublishSettingsName
from sh_edraft.utils import Console


class PublishSettingsModel(ConfigurationModelBase):

    def __init__(self):
        ConfigurationModelBase.__init__(self)

        self._source_path: Optional[str] = None
        self._dist_path: Optional[str] = None
        self._templates: Optional[list[Template]] = None

        self._included_files: Optional[list[str]] = None
        self._excluded_files: Optional[list[str]] = None

        self._template_ending: Optional[str] = None

    @property
    def source_path(self) -> str:
        return self._source_path

    @source_path.setter
    def source_path(self, source_path: str):
        self._source_path = source_path

    @property
    def dist_path(self) -> str:
        return self._dist_path

    @dist_path.setter
    def dist_path(self, dist_path: str):
        self._dist_path = dist_path

    @property
    def templates(self) -> list[Template]:
        return self._templates

    @templates.setter
    def templates(self, templates: list[Template]):
        self._templates = templates
        
    @property
    def included_files(self) -> list[str]:
        return self._included_files
    
    @included_files.setter
    def included_files(self, included_files: list[str]):
        self._included_files = included_files

    @property
    def excluded_files(self) -> list[str]:
        return self._excluded_files

    @excluded_files.setter
    def excluded_files(self, excluded_files: list[str]):
        self._excluded_files = excluded_files
        
    @property
    def template_ending(self) -> str:
        return self._template_ending
    
    @template_ending.setter
    def template_ending(self, template_ending: str):
        self._template_ending = template_ending

    def from_dict(self, settings: dict):
        try:
            self._source_path = settings[PublishSettingsName.source_path.value]
            self._dist_path = settings[PublishSettingsName.dist_path.value]
            self._templates = settings[PublishSettingsName.templates.value]
            self._included_files = settings[PublishSettingsName.included_files.value]
            self._excluded_files = settings[PublishSettingsName.excluded_files.value]
            self._template_ending = settings[PublishSettingsName.template_ending.value]
        except Exception as e:
            Console.write_line(
                f'[ ERROR ] [ {__name__} ]: Reading error in {PublishSettingsName.publish.value} settings', 'red')
            Console.write_line(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}', 'red')
