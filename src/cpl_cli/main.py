from typing import Type

import pkg_resources

from cpl_cli.cli import CLI
from cpl_cli.startup import Startup
from cpl_cli.startup_argument_extension import StartupArgumentExtension
from cpl_core.application.application_builder import ApplicationBuilder
from cpl_core.application.startup_extension_abc import StartupExtensionABC


def get_startup_extensions() -> list[Type[StartupExtensionABC]]:
    blacklisted_packages = ['cpl-cli']
    startup_extensions = []

    installed_packages = pkg_resources.working_set
    for p in installed_packages:
        package = str(p).split(' ')[0]
        if not package.startswith('cpl-') or package in blacklisted_packages:
            continue

        package = package.replace('-', '_')
        loaded_package = __import__(package)
        if '__cli_startup_extension__' not in dir(loaded_package):
            continue
        startup_extensions.append(loaded_package.__cli_startup_extension__)

    return startup_extensions


def main():
    app_builder = ApplicationBuilder(CLI)
    app_builder.use_startup(Startup)
    app_builder.use_extension(StartupArgumentExtension)
    for extension in get_startup_extensions():
        app_builder.use_extension(extension)

    app_builder.build().run()


if __name__ == '__main__':
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
