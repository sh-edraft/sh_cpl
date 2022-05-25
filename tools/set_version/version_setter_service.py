import json
import os

from cpl_core.environment import ApplicationEnvironmentABC


class VersionSetterService:

    def __init__(self, env: ApplicationEnvironmentABC):
        self._env = env

    def set_version(self, file: str, version: dict):
        project_json = {}
        with open(os.path.join(self._env.working_directory, file), 'r', encoding='utf-8') as f:
            # load json
            project_json = json.load(f)
            f.close()

        project_json['ProjectSettings']['Version'] = version
        with open(os.path.join(self._env.working_directory, file), 'w', encoding='utf-8') as f:
            f.write(json.dumps(project_json, indent=2))
            f.close()
