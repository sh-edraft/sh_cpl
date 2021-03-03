from cpl_cli.cli import CLI
from cpl_cli.startup import Startup

if __name__ == '__main__':
    cli = CLI()
    cli.use_startup(Startup)
    cli.build()
    cli.run()
