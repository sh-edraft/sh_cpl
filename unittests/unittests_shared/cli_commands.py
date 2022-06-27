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

        if output:
            subprocess.run(command, env=env_vars)
        else:
            subprocess.run(command, env=env_vars, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    @staticmethod
    def _run_with_output(cmd: str, *args) -> str:
        env_vars = os.environ
        env_vars['CPL_IS_UNITTEST'] = 'NO'

        command = ['python', CLI_PATH, cmd]
        for arg in args:
            command.append(arg)

        return subprocess.run(command, env=env_vars, check=True, capture_output=True, text=True).stdout

    @classmethod
    def add(cls, source: str, target: str, output=False):
        cls._run('add', source, target, output=output)

    @classmethod
    def build(cls, output=False):
        cls._run('build', output=output)

    @classmethod
    def generate(cls, schematic: str, name: str, output=False):
        cls._run('generate', schematic, name, output=output)

    @classmethod
    def install(cls, package: str = None, output=False):
        if package is None:
            cls._run('install', output=output)
            return

        cls._run('install', package, output=output)

    @classmethod
    def new(cls, project_type: str, name: str, *args, output=False):
        cls._run('new', project_type, name, *args, output=output)

    @classmethod
    def publish(cls, output=False):
        cls._run('publish', output=output)

    @classmethod
    def remove(cls, project: str, output=False):
        cls._run('remove', project, output=output)

    @classmethod
    def run(cls, project: str = None, output=False):
        if project is None:
            cls._run('run', output=output)
            return
        cls._run('run', project, output=output)

    @classmethod
    def start(cls, output=False):
        cls._run('start', output=output)

    @classmethod
    def uninstall(cls, package: str, output=False):
        cls._run('uninstall', package, output=output)

    @classmethod
    def update(cls, output=False):
        cls._run('update', output=output)

    @classmethod
    def version(cls) -> str:
        return cls._run_with_output('version')
