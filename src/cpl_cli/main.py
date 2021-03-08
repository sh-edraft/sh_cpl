from cpl_cli.cli import CLI
from cpl_cli.startup import Startup


def main():
    cli = CLI()
    cli.use_startup(Startup)
    cli.build()
    cli.run()
