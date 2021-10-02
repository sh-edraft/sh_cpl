from cpl_core.application.application_builder import ApplicationBuilder
from application import Application
from general.test_extension import TestExtension
from startup import Startup


def main():
    app_builder = ApplicationBuilder(Application)
    app_builder.use_startup(Startup)
    app_builder.use_extension(TestExtension)
    app_builder.build().run()


if __name__ == '__main__':
    main()
