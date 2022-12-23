import string

from cpl_core.console.console import Console
from cpl_core.utils.string import String


class TestService:

    def __init__(self):
        self._name = String.random_string(string.ascii_lowercase, 8)

    def run(self):
        Console.write_line(f'Im {self._name}')
