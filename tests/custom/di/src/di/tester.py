from cpl_core.console.console import Console
from di.test_abc import TestABC


class Tester:

    def __init__(self, t1: TestABC, t2: TestABC, t3: list[TestABC]):
        Console.write_line('Tester:')
        Console.write_line(t1, t2, t3)
