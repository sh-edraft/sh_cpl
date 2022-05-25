from cpl_core.application import ApplicationBuilder

from set_pip_url.application import Application
from set_pip_url.startup import Startup


def main():
    app_builder = ApplicationBuilder(Application)
    app_builder.use_startup(Startup)
    app_builder.build().run()


if __name__ == '__main__':
    main()
