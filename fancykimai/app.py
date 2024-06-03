import click
from fancykimai.commands import commands
from fancykimai.classes.click_groups import AliasedGroup

@click.group(cls=AliasedGroup)
def cli():
    pass

for command in commands:
    cli.add_command(command)

if __name__ == '__main__':  
    cli()