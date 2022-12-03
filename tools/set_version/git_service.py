import os

from cpl_core.environment import ApplicationEnvironmentABC
from git import Repo


class GitService:

    def __init__(self, env: ApplicationEnvironmentABC):
        self._env = env
        self._repo = Repo(env.working_directory)

    def get_active_branch_name(self) -> str:
        branch = self._repo.active_branch
        return branch.name

    def get_diff_files(self) -> list[str]:
        return [item.a_path for item in self._repo.index.diff(None)]
