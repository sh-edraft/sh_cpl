import subprocess
import sys
from contextlib import suppress
from typing import Optional


class Pip:

    @staticmethod
    def get_package(package: str) -> Optional[str]:
        result = None
        with suppress(Exception):
            result = subprocess.check_output([sys.executable, "-m", "pip", "show", package], stderr=subprocess.DEVNULL)

        if result is None:
            return None

        new_package: list[str] = str(result, 'utf-8').lower().split('\n')
        new_version = ''

        for atr in new_package:
            if 'version' in atr:
                new_version = atr.split(': ')[1]

        return f'{package}=={new_version}'

    @staticmethod
    def install(package: str, *args, source: str = None, stdout=None, stderr=None):
        pip_args = [sys.executable, "-m", "pip", "install", "--yes"]

        for arg in args:
            pip_args.append(arg)

        if source is not None:
            pip_args.append(f'--extra-index-url')
            pip_args.append(source)

        pip_args.append(package)
        subprocess.run(pip_args, stdout=stdout, stderr=stderr)

    @staticmethod
    def uninstall(package: str, stdout=None, stderr=None):
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "--yes", package], stdout=stdout, stderr=stderr)
