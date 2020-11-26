from sh_edraft.hosting.base.environment_base import EnvironmentBase
from sh_edraft.hosting.model.environment_name import EnvironmentName


class HostingEnvironment(EnvironmentBase):

    def __init__(self, name: EnvironmentName, crp: str):
        EnvironmentBase.__init__(self)

        self._name = name
        self._content_root_path = crp

    @property
    def name(self) -> EnvironmentName:
        return self._name

    @property
    def content_root_path(self) -> str:
        return self._content_root_path

