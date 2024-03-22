import click
from fancykimai.functions.kimai import kimai_request

@click.group(name='teams')
def teams_group():
    pass

@teams_group.command(name='list')
@click.option('-o', '--output', type=click.Choice(['table', 'json']), default='table', help='Output format')
def list_teams(output: str):
    r = kimai_request('api/teams')
    if output == 'table':
        click.echo('ID\tName')
        for team in r:
            click.echo(f'{team["id"]}\t{team["name"]}')
    else:
        click.echo(r)