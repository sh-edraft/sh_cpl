import filecmp
import json
import os
import shutil
import unittest

from cpl_core.utils import String

from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class PublishTestCase(unittest.TestCase):

    def __init__(self, methodName: str):
        unittest.TestCase.__init__(self, methodName)
        self._source = 'publish-test-source'
        self._project_file = f'src/{String.convert_to_snake_case(self._source)}/{self._source}.json'

    def _get_project_settings(self):
        with open(os.path.join(os.getcwd(), self._project_file), 'r', encoding='utf-8') as cfg:
            # load json
            project_json = json.load(cfg)
            cfg.close()

        return project_json

    def _save_project_settings(self, settings: dict):
        with open(os.path.join(os.getcwd(), self._project_file), 'w', encoding='utf-8') as project_file:
            project_file.write(json.dumps(settings, indent=2))
            project_file.close()

    def setUp(self):
        os.chdir(os.path.abspath(PLAYGROUND_PATH))
        # create projects
        CLICommands.new('console', self._source, '--ab', '--s')
        os.chdir(os.path.join(os.getcwd(), self._source))

    def cleanUp(self):
        # remove projects
        if not os.path.exists(os.path.abspath(os.path.join(PLAYGROUND_PATH, self._source))):
            return

        shutil.rmtree(os.path.abspath(os.path.join(PLAYGROUND_PATH, self._source)))

    def _are_dir_trees_equal(self, dir1, dir2):
        """
        found at https://stackoverflow.com/questions/4187564/recursively-compare-two-directories-to-ensure-they-have-the-same-files-and-subdi

        Compare two directories recursively. Files in each directory are
        assumed to be equal if their names and contents are equal.

        @param dir1: First directory path
        @param dir2: Second directory path

        @return: True if the directory trees are the same and
            there were no errors while accessing the directories or files,
            False otherwise.
       """

        dirs_cmp = filecmp.dircmp(dir1, dir2)
        if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or len(dirs_cmp.funny_files) > 0:
            return False

        (_, mismatch, errors) = filecmp.cmpfiles(dir1, dir2, dirs_cmp.common_files, shallow=False)

        if len(mismatch) > 0 or len(errors) > 0:
            return False

        for common_dir in dirs_cmp.common_dirs:
            new_dir1 = os.path.join(dir1, common_dir)
            new_dir2 = os.path.join(dir2, common_dir)
            if not self._are_dir_trees_equal(new_dir1, new_dir2):
                return False

        return True

    def test_publish(self):
        CLICommands.publish()
        dist_path = './dist'
        setup_path = f'{dist_path}/{self._source}/publish/setup'
        full_dist_path = f'{dist_path}/{self._source}/publish/'
        self.assertTrue(os.path.exists(dist_path))
        self.assertTrue(os.path.exists(setup_path))
        self.assertTrue(os.path.exists(os.path.join(setup_path, f'{self._source}-0.0.0.tar.gz')))
        self.assertTrue(os.path.exists(os.path.join(setup_path, f'{String.convert_to_snake_case(self._source)}-0.0.0-py3-none-any.whl')))
        self.assertTrue(os.path.exists(full_dist_path))
        self.assertFalse(self._are_dir_trees_equal(f'./src/{String.convert_to_snake_case(self._source)}', full_dist_path))
        with open(f'{full_dist_path}/{self._source}.json', 'w') as file:
            file.write(json.dumps(self._get_project_settings(), indent=2))
            file.close()
        # self.assertTrue(self._are_dir_trees_equal(f'./src/{String.convert_to_snake_case(self._source)}', full_dist_path))
