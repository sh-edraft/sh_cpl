from tests.Application import Application
from tests.startup import Startup

if __name__ == '__main__':
    app = Application()
    app.use_startup(Startup)
    app.build()
    app.run()
