from application import Application
from cpl_core.application import ApplicationBuilder
from test_extension import TestExtension
from startup import Startup
from test_startup_extension import TestStartupExtension


def main():
    app_builder = ApplicationBuilder(Application)
    app_builder.use_startup(Startup)
    app_builder.use_extension(TestStartupExtension)
    app_builder.use_extension(TestExtension)
    app_builder.build().run()


if __name__ == '__main__':
    main()
