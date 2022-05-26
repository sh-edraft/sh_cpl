import os
import subprocess

from unittests_cli.constants import CLI_PATH


class CLICommands:

    @staticmethod
    def _run(cmd: str, *args):
        env_vars = os.environ
        # env_vars['CPL_IS_UNITTEST'] = 'YES'
        command = ['python', CLI_PATH, cmd]
        for arg in args:
            command.append(arg)

        subprocess.run(command, env=env_vars)

    @classmethod
    def generate(cls, schematic: str, name: str):
        cls._run('generate', schematic, name)

    @classmethod
    def new(cls, project_type: str, name: str, *args):
        cls._run('new', project_type, name, *args)
