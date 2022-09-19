import os
import subprocess
import sys
from contextlib import suppress
from typing import Optional

from cpl_core.console import Console


class Pip:
    r"""Executes pip commands"""
    _executable = sys.executable
    _env = os.environ

    """Getter"""

    @classmethod
    def get_executable(cls) -> str:
        return cls._executable

    """Setter"""

    @classmethod
    def set_executable(cls, executable: str):
        r"""Sets the executable

        Parameter
        ---------
            executable: :class:`str`
                The python command
        """
        if executable is None or executable == sys.executable:
            return

        cls._executable = executable
        if not os.path.islink(cls._executable):
            return

        path = os.path.dirname(os.path.dirname(cls._executable))
        cls._env = os.environ
        if sys.platform == 'win32':
            cls._env['PATH'] = f'{path}\\bin' + os.pathsep + os.environ.get('PATH', '')
        else:
            cls._env['PATH'] = f'{path}/bin' + os.pathsep + os.environ.get('PATH', '')
        cls._env['VIRTUAL_ENV'] = path

    @classmethod
    def reset_executable(cls):
        r"""Resets the executable to system standard"""
        cls._executable = sys.executable

    """Public utils functions"""

    @classmethod
    def get_package(cls, package: str) -> Optional[str]:
        r"""Gets given package py local pip list

        Parameter
        ---------
            package: :class:`str`

        Returns
        -------
            The package name as string
        """
        result = None
        with suppress(Exception):
            args = [cls._executable, "-m", "pip", "freeze"]

            result = subprocess.check_output(
                args,
                stderr=subprocess.DEVNULL, env=cls._env
            )

        if result is None:
            return None

        for p in str(result.decode()).split('\n'):
            if p == package:
                return p

        return None

    @classmethod
    def get_outdated(cls) -> bytes:
        r"""Gets table of outdated packages

        Returns
        -------
            Bytes string of the command result
        """
        args = [cls._executable, "-m", "pip", "list", "--outdated"]

        return subprocess.check_output(args, env=cls._env)

    @classmethod
    def install(cls, package: str, *args, source: str = None, stdout=None, stderr=None):
        r"""Installs given package

        Parameter
        ---------
            package: :class:`str`
                The name of the package
            args: :class:`list`
                Arguments for the command
            source: :class:`str`
                Extra index URL
            stdout: :class:`str`
                Stdout of subprocess.run
            stderr: :class:`str`
                Stderr of subprocess.run
        """
        pip_args = [cls._executable, "-m", "pip", "install"]

        for arg in args:
            pip_args.append(arg)

        pip_args.append(package)

        if source is not None:
            pip_args.append(f'--extra-index-url')
            pip_args.append(source)
        subprocess.run(pip_args, stdout=stdout, stderr=stderr, env=cls._env)

    @classmethod
    def uninstall(cls, package: str, stdout=None, stderr=None):
        r"""Uninstalls given package

        Parameter
        ---------
            package: :class:`str`
                The name of the package
            stdout: :class:`str`
                Stdout of subprocess.run
            stderr: :class:`str`
                Stderr of subprocess.run
        """
        args = [cls._executable, "-m", "pip", "uninstall", "--yes", package]

        subprocess.run(
            args,
            stdout=stdout, stderr=stderr, env=cls._env
        )
