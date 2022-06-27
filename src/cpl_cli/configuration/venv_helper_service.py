import os
import subprocess
import sys


class VenvHelper:

    @staticmethod
    def create_venv(path):
        subprocess.run(
            [sys.executable, '-m', 'venv', os.path.abspath(os.path.join(path, '../../'))],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
