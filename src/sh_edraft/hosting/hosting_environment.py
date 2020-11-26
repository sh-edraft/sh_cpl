from typing import Optional

from sh_edraft.hosting.base.environment_base import EnvironmentBase
from sh_edraft.hosting.model.environment_name import EnvironmentName


class HostingEnvironment(EnvironmentBase):

    def __init__(self, name: EnvironmentName = EnvironmentName.production, crp: str = './'):
        EnvironmentBase.__init__(self)

        self._name: Optional[EnvironmentName] = name
        self._content_root_path: Optional[str] = crp

    @property
    def name(self) -> EnvironmentName:
        return self._name

    @name.setter
    def name(self, name: EnvironmentName):
        self._name = name

    @property
    def content_root_path(self) -> str:
        return self._content_root_path

    @content_root_path.setter
    def content_root_path(self, content_root_path: str):
        self._content_root_path = content_root_path
