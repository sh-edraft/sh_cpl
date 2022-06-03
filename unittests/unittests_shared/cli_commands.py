import os
import subprocess

from unittests_cli.constants import CLI_PATH


class CLICommands:

    @staticmethod
    def _run(cmd: str, *args, output=False):
        env_vars = os.environ
        env_vars['CPL_IS_UNITTEST'] = 'NO' if output else 'YES'

        command = ['python', CLI_PATH, cmd]
        for arg in args:
            command.append(arg)

        subprocess.run(command, env=env_vars)

    @classmethod
    def add(cls, source: str, target: str):
        cls._run('add', source, target)

    @classmethod
    def generate(cls, schematic: str, name: str, output=False):
        cls._run('generate', schematic, name, output=output)

    @classmethod
    def new(cls, project_type: str, name: str, *args, output=False):
        cls._run('new', project_type, name, *args, output=output)

    @classmethod
    def remove(cls, project: str):
        cls._run('remove', project)
