import string
from cpl_core.console.console import Console
from cpl_core.utils.string import String
from di.test_abc import TestABC


class Test1Service(TestABC):

    def __init__(self):
        TestABC.__init__(self, String.random_string(string.ascii_lowercase, 8))

    def run(self):
        Console.write_line(f'Im {self._name}')
