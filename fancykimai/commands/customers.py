import click
from fancykimai.functions.kimai import kimai_request
from rich import table, console
import json

@click.group(name='customers')
def customers_group():
    """
    Customer commands
    """
    pass

@customers_group.command(name='list')
@click.option('-o', '--output', type=click.Choice(['table', 'json']), default='table', help='Output format')
def list_customers(output: str):
    """
    List customers
    """
    r = kimai_request('api/customers')
    if output == 'table':
        columns = [
            {'column': "ID", 'response_key': 'id', 'function': str, 'style': 'cyan'},
            {'column': "Name", 'response_key': 'name', 'function': str, 'style': 'magenta'},
        ]
        rich_table = table.Table(title="Customers")
        for column in columns:
            rich_table.add_column(column['column'], style=column['style'])
        for customer in r:
            rich_table.add_row(*[column['function'](customer[column['response_key']]) for column in columns])
        rich_console = console.Console()
        rich_console.print(rich_table)
    else:
        click.echo(json.dumps(r))