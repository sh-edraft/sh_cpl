from typing import List

from sh_edraft.common.interface.ipublisher import IPublisher
from sh_edraft.publish.model.template import Template


class Publisher(IPublisher):

    def __init__(self, local_path: str):
        super().__init__(local_path)
        self._local_path = local_path
        self._templates: List[Template] = []

    @property
    def local_path(self) -> str:
        return self._local_path

    def create(self, templates: List[Template]):
        self._templates = templates

    def publish(self):
        print(self._local_path, [(t.name, t.path) for t in self._templates])
