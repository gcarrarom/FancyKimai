import click
import os
from fancykimai.functions.config import get_config, set_config, unset_config
from fancykimai.classes.click_groups import AliasedGroup

@click.group(name="config", cls=AliasedGroup)
def config_group():
    """
    Configuration commands
    """
    pass

@config_group.command()
def show():
    """
    Show the configuration file
    """
    config_file = os.path.expanduser("~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config_data = f.read()
            click.echo(config_data)
    else:
        click.echo("Configuration file not found.")

@config_group.command()
@click.argument("key")
@click.argument("value")
@click.option("--context", help="Set the configuration value for a specific context", default=None, required=False)
def set(key, value, context):
    """
    Set a configuration value
    """
    set_config(key, value, context=context)
    click.echo(f"Set {key} to {value}")

@config_group.command()
@click.argument("key")
@click.option("--context", help="Unset the configuration value for a specific context", default=None, required=False)
def get(key, context):
    """
    Get a configuration value
    """
    click.echo(get_config(key, context=context))

@config_group.command()
@click.argument("key")
@click.option("--context", help="Unset the configuration value for a specific context", default=None, required=False)
def unset(key,  context):
    """
    Unset a configuration value
    """
    unset_config(key, context=context)
    click.echo(f"Unset {key}")