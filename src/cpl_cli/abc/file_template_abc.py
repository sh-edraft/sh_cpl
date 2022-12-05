from abc import ABC, abstractmethod

from cpl_core.utils import String


class FileTemplateABC(ABC):

    @abstractmethod
    def __init__(self, name: str, path: str, code: str):
        self._name = f'{String.convert_to_snake_case(name)}.py'
        self._path = path
        self._code = code

    def __repr__(self):
        return f'<{type(self).__name__} {self._path}{self._name}>'

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path
    
    @path.setter
    def path(self, value: str):
        self._path = value

    @property
    def value(self) -> str:
        return self.get_code()

    @abstractmethod
    def get_code(self) -> str: pass
