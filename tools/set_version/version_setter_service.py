import json
import os

from cpl_core.console import Console

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
        dependencies = project_json['ProjectSettings']['Dependencies']
        new_deps = []
        for dependency in dependencies:
            if not dependency.startswith('cpl-'):
                new_deps.append(dependency)
                continue

            dep_version = dependency.split('=')[1]
            new_deps.append(dependency.replace(dep_version, f'{version["Major"]}.{version["Minor"]}.{version["Micro"]}'))

        project_json['ProjectSettings']['Dependencies'] = new_deps

        with open(os.path.join(self._env.working_directory, file), 'w', encoding='utf-8') as f:
            f.write(json.dumps(project_json, indent=2))
            f.close()
