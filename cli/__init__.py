import click

import config
from cli.commands import add_cli_commands


@click.group()
def cli():
    pass


add_cli_commands(cli)
