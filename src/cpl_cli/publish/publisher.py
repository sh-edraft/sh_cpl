import os
import shutil

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.console.console import Console
from cpl_cli.publish.project_settings import ProjectSettings
from cpl_cli.publish.publisher_abc import PublisherABC


class Publisher(PublisherABC):

    def __init__(self, runtime: ApplicationRuntimeABC, project: ProjectSettings):
        PublisherABC.__init__(self)

        self._runtime = runtime

        self._project = project

    @property
    def source_path(self) -> str:
        return ''

    @property
    def dist_path(self) -> str:
        return ''

    def _create_dist_path(self):
        self._project.dist_path = os.path.join(self._runtime.working_directory, self._project.dist_path)

        Console.write_line('DIST:', self._project.dist_path)

        if os.path.isdir(self._project.dist_path):
            try:
                shutil.rmtree(self._project.dist_path)
            except Exception as e:
                Console.error(f'{e}')
                exit()

        if not os.path.isdir(self._project.dist_path):
            try:
                os.makedirs(self._project.dist_path)
            except Exception as e:
                Console.error(f'{e}')
                exit()

    def _create_packages(self):
        pass

    def _dist_files(self):
        pass

    def include(self, path: str):
        pass

    def exclude(self, path: str):
        pass

    def build(self):
        Console.write_line('Creating internal packages:')
        self._create_packages()
        Console.write_line('Building application:')
        self._dist_files()

    def publish(self):
        pass
