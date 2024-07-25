import importlib.metadata
from typing import Type

from cpl_cli.cli import CLI
from cpl_cli.startup import Startup
from cpl_cli.startup_argument_extension import StartupArgumentExtension
from cpl_cli.startup_migration_extension import StartupMigrationExtension
from cpl_cli.startup_workspace_extension import StartupWorkspaceExtension
from cpl_core.application.application_builder import ApplicationBuilder
from cpl_core.application.startup_extension_abc import StartupExtensionABC
from cpl_core.console import Console


def get_startup_extensions() -> list[Type[StartupExtensionABC]]:
    blacklisted_packages = ["cpl-cli"]
    startup_extensions = []

    installed_packages = importlib.metadata.distributions()
    for p in installed_packages:
        if not p.name.startswith("cpl-") or p.name in blacklisted_packages:
            continue

        package = p.name.replace("-", "_")
        loaded_package = __import__(package)
        if "__cli_startup_extension__" not in dir(loaded_package):
            continue
        startup_extensions.append(loaded_package.__cli_startup_extension__)

    return startup_extensions


def main():
    app_builder = ApplicationBuilder(CLI)
    app_builder.use_startup(Startup)
    app_builder.use_extension(StartupWorkspaceExtension)
    app_builder.use_extension(StartupArgumentExtension)
    app_builder.use_extension(StartupMigrationExtension)
    for extension in get_startup_extensions():
        app_builder.use_extension(extension)

    app_builder.build().run()
    Console.write_line()


if __name__ == "__main__":
    main()

#         ((
#         ( `)
#         ; / ,
#        /  \/
#       /  |
#      /  ~/
#     / )  )   ~ edraft
# ___// | /
# `--'  \_~-,
