from cpl.application.application_builder import ApplicationBuilder
from tests.custom.general.application import Application
from tests.custom.general.startup import Startup


def main():
    app_builder = ApplicationBuilder(Application)
    app_builder.use_startup(Startup)
    app_builder.build().run()


if __name__ == '__main__':
    main()
