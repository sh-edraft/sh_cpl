from cpl_core.console.console import Console
from test_service_service import TestService


class DITesterService:

    def __init__(self, ts: TestService):
        self._ts = ts
    
    def run(self):
        Console.write_line('DIT: ')
        self._ts.run()
