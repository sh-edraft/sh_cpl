from application import Application
from cpl_core.application import ApplicationBuilder
from general.test_extension import TestExtension
from startup import Startup


def main():
    app_builder = ApplicationBuilder(Application)
    app_builder.use_startup(Startup)
    app_builder.use_extension(TestExtension)
    app_builder.build().run()


if __name__ == '__main__':
    main()
