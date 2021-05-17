import os
import subprocess
import sys
from contextlib import suppress
from typing import Optional


class Pip:
    r"""Executes pip commands"""
    _executable = sys.executable
    _env = os.environ
    _is_venv = False

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
        r"""Resets the executable to system standard"""
        cls._executable = sys.executable
        cls._is_venv = False

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
        r"""Gets table of outdated packages

        Returns
        -------
            Bytes string of the command result
        """
        args = [cls._executable, "-m", "pip", "list", "--outdated"]
        if cls._is_venv:
            args = ["pip", "list", "--outdated"]

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
        if cls._is_venv:
            args = ["pip", "uninstall", "--yes", package]

        subprocess.run(
            args,
            stdout=stdout, stderr=stderr, env=cls._env
        )
