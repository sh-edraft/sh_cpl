import os
import subprocess

from unittests_cli.constants import CLI_PATH


class CLICommands:

    @staticmethod
    def _run(cmd: str, *args):
        env_vars = os.environ
        command = ['python', CLI_PATH, cmd]
        for arg in args:
            command.append(arg)

        print(f'Running {command}')
        subprocess.run(command, env=env_vars)

    @classmethod
    def generate(cls, *args):
        cls._run('generate', *args)

    @classmethod
    def new(cls, *args):
        cls._run('new', *args)
