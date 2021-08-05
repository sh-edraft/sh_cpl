import traceback
from typing import Optional

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.console import Console
from cpl_cli.configuration.workspace_settings_name_enum import WorkspaceSettingsNameEnum


class WorkspaceSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)
        
        self._default_project: Optional[str] = None
        self._projects: dict[str, str] = {}
        self._scripts: dict[str, str] = {}
        
    @property
    def default_project(self) -> str:
        return self._default_project

    @property
    def projects(self) -> dict[str, str]:
        return self._projects

    @property
    def scripts(self):
        return self._scripts

    def from_dict(self, settings: dict):
        try:
            self._default_project = settings[WorkspaceSettingsNameEnum.default_project.value]
            self._projects = settings[WorkspaceSettingsNameEnum.projects.value]

            if WorkspaceSettingsNameEnum.scripts.value in settings:
                self._scripts = settings[WorkspaceSettingsNameEnum.scripts.value]
            else:
                self._scripts = {}
        except Exception as e:
            Console.error(f'[ ERROR ] [ {__name__} ]: Reading error in {self.__name__} settings')
            Console.error(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
