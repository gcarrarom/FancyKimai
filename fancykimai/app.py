import click
from fancykimai.commands import commands

@click.group()
def cli():
    pass

for command in commands:
    cli.add_command(command)

if __name__ == '__main__':
    cli()