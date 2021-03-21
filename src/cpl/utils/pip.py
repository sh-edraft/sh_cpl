import subprocess
import sys
from contextlib import suppress
from typing import Optional


class Pip:
    """
    Executes pip commands
    """
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
        """
        Sets the executable
        :param executable:
        :return:
        """
        if executable is not None:
            cls._executable = executable

    @classmethod
    def reset_executable(cls):
        """
        Resets the executable to system standard
        :return:
        """
        cls._executable = sys.executable

    """
        Public utils functions
    """

    @classmethod
    def get_package(cls, package: str) -> Optional[str]:
        """
        Gets given package py local pip list
        :param package:
        :return:
        """
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

        if new_version != '':
            return f'{package}=={new_version}'

        return package

    @classmethod
    def get_outdated(cls) -> bytes:
        """
        Gets table of outdated packages
        :return:
        """
        return subprocess.check_output([cls._executable, "-m", "pip", "list", "--outdated"])

    @classmethod
    def install(cls, package: str, *args, source: str = None, stdout=None, stderr=None):
        """
        Installs given package
        :param package:
        :param args:
        :param source:
        :param stdout:
        :param stderr:
        :return:
        """
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
        """
        Uninstalls given package
        :param package:
        :param stdout:
        :param stderr:
        :return:
        """
        subprocess.run([cls._executable, "-m", "pip", "uninstall", "--yes", package], stdout=stdout, stderr=stderr)
