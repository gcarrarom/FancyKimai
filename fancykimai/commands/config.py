import click
import os
from fancykimai.functions.config import get_config, set_config

@click.group(name="config")
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
def set(key, value):
    """
    Set a configuration value
    """
    set_config(key, value)
    click.echo(f"Set {key} to {value}")

@config_group.command()
@click.argument("key")
def get(key):
    """
    Get a configuration value
    """
    click.echo(get_config(key))