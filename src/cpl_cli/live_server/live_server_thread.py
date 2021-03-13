import os
import subprocess
import sys
import threading
from datetime import datetime

from cpl.console import Console


class LiveServerThread(threading.Thread):

    def __init__(self, path: str):
        threading.Thread.__init__(self)

        self._path = path
        self._main = ''
        self._command = []
        
    @property
    def command(self) -> list[str]:
        return self._command
    
    @property
    def main(self) -> str:
        return self._main

    def run(self):
        self._main = os.path.join(self._path, 'main.py')
        if not os.path.isfile(self._main):
            Console.error('Entry point main.py not found')
            return

        Console.write_line('Read successfully')
        now = datetime.now()
        Console.write_line(f'Started at {now.strftime("%Y-%m-%d %H:%M:%S")}\n\n')

        self._command = [sys.executable, self._main, ''.join(sys.argv[2:])]
        subprocess.run(self._command)
