from cpl_cli.startup_argument_extension import StartupArgumentExtension
from cpl_core.application.application_builder import ApplicationBuilder
from cpl_cli.cli import CLI
from cpl_cli.startup import Startup


def main():
    app_builder = ApplicationBuilder(CLI)
    app_builder.use_startup(Startup)
    app_builder.use_extension(StartupArgumentExtension)
    app_builder.build().run()


if __name__ == '__main__':
    main()
