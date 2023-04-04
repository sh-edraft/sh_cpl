import os

base = ""
if not os.getcwd().endswith("unittests"):
    base = "../"

PLAYGROUND_PATH = os.path.abspath(os.path.join(os.getcwd(), f"{base}test_cli_playground"))
TRANSLATION_PATH = os.path.abspath(os.path.join(os.getcwd(), f"{base}unittests_translation"))
CLI_PATH = os.path.abspath(os.path.join(os.getcwd(), f"{base}../src/cpl_cli/main.py"))
