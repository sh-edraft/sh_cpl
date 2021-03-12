from tests.custom.general.application import Application
from tests.custom.general.startup import Startup


def main():
    app = Application()
    app.use_startup(Startup)
    app.build()
    app.run()


if __name__ == '__main__':
    main()
