import json
import os
from string import ascii_letters

from cpl_core.environment import ApplicationEnvironmentABC
from cpl_core.utils import String


class VersionSetterService:
    def __init__(self, env: ApplicationEnvironmentABC):
        self._env = env

    def _read_file(self, file: str) -> dict:
        project_json = {}
        with open(os.path.join(self._env.working_directory, file), "r", encoding="utf-8") as f:
            # load json
            project_json = json.load(f)
            f.close()

        return project_json

    def _write_file(self, file: str, project_json: dict):
        with open(os.path.join(self._env.working_directory, file), "w", encoding="utf-8") as f:
            f.write(json.dumps(project_json, indent=2))
            f.close()

    def set_version(self, file: str, version: dict):
        project_json = self._read_file(file)
        project_json["ProjectSettings"]["Version"] = version
        self._write_file(file, project_json)

    def set_dependencies(self, file: str, version: dict, key: str, skipped=None):
        project_json = self._read_file(file)
        if key not in project_json["ProjectSettings"]:
            project_json["ProjectSettings"][key] = []

        dependencies = project_json["ProjectSettings"][key]
        new_deps = []
        for dependency in dependencies:
            if not dependency.startswith("cpl-"):
                new_deps.append(dependency)
                continue

            dep_version = dependency.split("=")[1]
            dep_name = dependency.split("=")[0]
            if dep_name[len(dep_name) - 1] not in ascii_letters:
                dep_name = dep_name[: len(dep_name) - 1]

            if (
                skipped is not None
                and (dep_name in skipped or String.convert_to_snake_case(dep_name) in skipped)
                or dep_version == ""
            ):
                new_deps.append(dependency)
                continue

            new_deps.append(
                dependency.replace(dep_version, f'{version["Major"]}.{version["Minor"]}.{version["Micro"]}')
            )

        project_json["ProjectSettings"][key] = new_deps
        self._write_file(file, project_json)
