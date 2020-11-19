from typing import Optional


class Template:

    def __init__(self, name: Optional[str] = None, path: Optional[str] = None):
        self._name: Optional[str] = name
        self._path: Optional[str] = path

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path
