import traceback
from typing import Optional

from cpl_cli.configuration.workspace_settings_name_enum import WorkspaceSettingsNameEnum
from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.console import Console


class WorkspaceSettings(ConfigurationModelABC):
    def __init__(
        self,
        default_project: str = None,
        projects: dict = None,
        scripts: dict = None,
    ):
        ConfigurationModelABC.__init__(self)

        self._default_project: Optional[str] = default_project
        self._projects: dict[str, str] = {} if projects is None else projects
        self._scripts: dict[str, str] = {} if scripts is None else scripts

    @property
    def default_project(self) -> str:
        return self._default_project

    @property
    def projects(self) -> dict[str, str]:
        return self._projects

    @property
    def scripts(self):
        return self._scripts
