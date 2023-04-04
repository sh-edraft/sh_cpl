import filecmp
import json
import os
import shutil

from cpl_core.utils import String
from unittests_cli.abc.command_test_case import CommandTestCase
from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class PublishTestCase(CommandTestCase):
    def __init__(self, method_name: str):
        CommandTestCase.__init__(self, method_name)
        self._source = "publish-test-source"
        self._project_file = f"src/{String.convert_to_snake_case(self._source)}/{self._source}.json"

    def setUp(self):
        if not os.path.exists(PLAYGROUND_PATH):
            os.makedirs(PLAYGROUND_PATH)

        os.chdir(PLAYGROUND_PATH)
        # create projects
        CLICommands.new("console", self._source, "--ab", "--s")
        os.chdir(os.path.join(os.getcwd(), self._source))

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
        dist_path = "./dist"
        setup_path = f"{dist_path}/{self._source}/publish/setup"
        full_dist_path = f"{dist_path}/{self._source}/publish/build/lib/{String.convert_to_snake_case(self._source)}"
        self.assertTrue(os.path.exists(dist_path))
        self.assertTrue(os.path.exists(setup_path))
        self.assertTrue(os.path.exists(os.path.join(setup_path, f"{self._source}-0.0.0.tar.gz")))
        self.assertTrue(
            os.path.exists(
                os.path.join(setup_path, f"{String.convert_to_snake_case(self._source)}-0.0.0-py3-none-any.whl")
            )
        )
        self.assertTrue(os.path.exists(full_dist_path))
        self.assertFalse(
            self._are_dir_trees_equal(f"./src/{String.convert_to_snake_case(self._source)}", full_dist_path)
        )

        shutil.copyfile(os.path.join(os.getcwd(), self._project_file), f"{full_dist_path}/{self._source}.json")
        shutil.copyfile(
            os.path.join(os.getcwd(), os.path.dirname(self._project_file), "appsettings.json"),
            f"{full_dist_path}/appsettings.json",
        )

        self.assertTrue(
            self._are_dir_trees_equal(f"./src/{String.convert_to_snake_case(self._source)}", full_dist_path)
        )
