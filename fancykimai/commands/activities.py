import click
from fancykimai.functions.kimai import kimai_request
from rich import table, console
import json

@click.group(name='activities')
def activities_group():
    pass

@activities_group.command(name='list')
@click.option('-o', '--output', type=click.Choice(['table', 'json']), default='table', help='Output format')
def list_activities(output: str):
    r = kimai_request('api/activities')
    if output == 'table':
        columns = [
            {'column': "ID", 'response_key': 'id', 'function': str, 'style': 'cyan'},
            {'column': "Name", 'response_key': 'name', 'function': str, 'style': 'magenta'},
        ]
        rich_table = table.Table(title="Activities")
        for column in columns:
            rich_table.add_column(column['column'], style=column['style'])
        for activity in r:
            rich_table.add_row(*[column['function'](activity[column['response_key']]) for column in columns])
        rich_console = console.Console()
        rich_console.print(rich_table)
    else:
        click.echo(json.dumps(r))