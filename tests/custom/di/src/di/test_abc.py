from abc import ABC


class TestABC(ABC):

    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return f'<{type(self).__name__} {self._name}>'
