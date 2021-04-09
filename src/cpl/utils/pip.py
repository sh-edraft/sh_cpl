import os
import subprocess
import sys
import shlex
from contextlib import suppress
from textwrap import dedent
from typing import Optional


class Pip:
    """
    Executes pip commands
    """
    _executable = sys.executable
    _env = os.environ
    _is_venv = False

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
        if executable is not None and executable != sys.executable:
            cls._executable = executable
            if os.path.islink(cls._executable):
                cls._is_venv = True
                path = os.path.dirname(os.path.dirname(cls._executable))
                cls._env = os.environ
                if sys.platform == 'win32':
                    cls._env['PATH'] = f'{path}\\bin' + os.pathsep + os.environ.get('PATH', '')
                else:
                    cls._env['PATH'] = f'{path}/bin' + os.pathsep + os.environ.get('PATH', '')
                cls._env['VIRTUAL_ENV'] = path

    @classmethod
    def reset_executable(cls):
        """
        Resets the executable to system standard
        :return:
        """
        cls._executable = sys.executable
        cls._is_venv = False

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
            args = [cls._executable, "-m", "pip", "show", package]
            if cls._is_venv:
                args = ["pip", "show", package]

            result = subprocess.check_output(
                args,
                stderr=subprocess.DEVNULL, env=cls._env
            )

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
        args = [cls._executable, "-m", "pip", "list", "--outdated"]
        if cls._is_venv:
            args = ["pip", "list", "--outdated"]

        return subprocess.check_output(args, env=cls._env)

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
        if cls._is_venv:
            pip_args = ["pip", "install"]

        for arg in args:
            pip_args.append(arg)

        if source is not None:
            pip_args.append(f'--extra-index-url')
            pip_args.append(source)

        pip_args.append(package)
        subprocess.run(pip_args, stdout=stdout, stderr=stderr, env=cls._env)

    @classmethod
    def uninstall(cls, package: str, stdout=None, stderr=None):
        """
        Uninstalls given package
        :param package:
        :param stdout:
        :param stderr:
        :return:
        """
        args = [cls._executable, "-m", "pip", "uninstall", "--yes", package]
        if cls._is_venv:
            args = ["pip", "uninstall", "--yes", package]

        subprocess.run(
            args,
            stdout=stdout, stderr=stderr, env=cls._env
        )
