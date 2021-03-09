from startup import Startup
from application import Application


def main():
    app = Application()
    app.use_startup(Startup)
    app.build()
    app.run()


if __name__ == '__main__':
    main()
