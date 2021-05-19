from cpl.application import ApplicationBuilder

from simple_app.application import Application


def main():
    app_builder = ApplicationBuilder(Application)
    app_builder.build().run()


if __name__ == '__main__':
    main()
