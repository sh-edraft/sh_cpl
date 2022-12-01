import os
import shutil
import traceback
import unittest

from unittests_cli.constants import PLAYGROUND_PATH


class CommandTestCase(unittest.TestCase):

    def __init__(self, method_name: str):
        unittest.TestCase.__init__(self, method_name)

    @classmethod
    def setUpClass(cls):

        try:
            if os.path.exists(PLAYGROUND_PATH):
                shutil.rmtree(os.path.abspath(os.path.join(PLAYGROUND_PATH)))

            os.makedirs(PLAYGROUND_PATH)
            os.chdir(PLAYGROUND_PATH)
        except Exception as e:
            print(f'Setup of {__name__} failed: {traceback.format_exc()}')

    def setUp(self):
        os.chdir(PLAYGROUND_PATH)

    @classmethod
    def tearDownClass(cls):
        try:
            if os.path.exists(PLAYGROUND_PATH):
                shutil.rmtree(os.path.abspath(os.path.join(PLAYGROUND_PATH)))
        except Exception as e:
            print(f'Cleanup of {__name__} failed: {traceback.format_exc()}')
