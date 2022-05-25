import os

from cpl_core.environment import ApplicationEnvironmentABC


class GitService:

    def __init__(self, env: ApplicationEnvironmentABC):
        self._env = env

    def get_active_branch_name(self) -> str:
        head_dir = os.path.join(self._env.working_directory, '.git/HEAD')
        with open(head_dir, 'r') as f:
            content = f.read().splitlines()

        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]
