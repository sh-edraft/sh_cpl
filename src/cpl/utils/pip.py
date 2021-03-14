import subprocess
import sys
from contextlib import suppress
from typing import Optional


class Pip:
    _executable = sys.executable

    """
        Getter
    """

    @classmethod
    def get_executable(cls) -> str:
        return cls._executable

    """
        Setter
    """

    @classmethod
    def set_executable(cls, executable: str):
        if executable is not None:
            cls._executable = executable

    @classmethod
    def reset_executable(cls):
        cls._executable = sys.executable

    """
        Public utils functions
    """

    @classmethod
    def get_package(cls, package: str) -> Optional[str]:
        result = None
        with suppress(Exception):
            result = subprocess.check_output([cls._executable, "-m", "pip", "show", package], stderr=subprocess.DEVNULL)

        if result is None:
            return None

        new_package: list[str] = str(result, 'utf-8').lower().split('\n')
        new_version = ''

        for atr in new_package:
            if 'version' in atr:
                new_version = atr.split(': ')[1]

        return f'{package}=={new_version}'

    @classmethod
    def get_outdated(cls) -> bytes:
        return subprocess.check_output([cls._executable, "-m", "pip", "list", "--outdated"])

    @classmethod
    def install(cls, package: str, *args, source: str = None, stdout=None, stderr=None):
        pip_args = [cls._executable, "-m", "pip", "install"]

        for arg in args:
            pip_args.append(arg)

        if source is not None:
            pip_args.append(f'--extra-index-url')
            pip_args.append(source)

        pip_args.append(package)
        subprocess.run(pip_args, stdout=stdout, stderr=stderr)

    @classmethod
    def uninstall(cls, package: str, stdout=None, stderr=None):
        subprocess.run([cls._executable, "-m", "pip", "uninstall", "--yes", package], stdout=stdout, stderr=stderr)
