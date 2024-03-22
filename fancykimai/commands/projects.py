import click
from fancykimai.functions.kimai import kimai_request
from fancykimai.functions.config import set_config
from rich import table, console
import json
from iterfzf import iterfzf

@click.group(name='projects')
def projects_group():
    pass

@projects_group.command(name='list')
@click.option('-o', '--output', type=click.Choice(['table', 'json']), default='table', help='Output format')
def list_projects(output: str):
    r = kimai_request('api/projects')
    if output == 'table':
        columns = [
            {'column': "ID", 'response_key': 'id', 'function': str, 'style': 'cyan'},
            {'column': "Name", 'response_key': 'name', 'function': str, 'style': 'magenta'},
        ]
        rich_table = table.Table(title="Projects")
        for column in columns:
            rich_table.add_column(column['column'], style=column['style'])
        for project in r:
            rich_table.add_row(*[column['function'](project[column['response_key']]) for column in columns])
        rich_console = console.Console()
        rich_console.print(rich_table)
    else:
        click.echo(json.dumps(r))

@projects_group.command(name='select')
@click.argument('project_id', type=int, required=False)
def select_project(project_id: int):
    if project_id is None:
        # get all projects
        projects = kimai_request('api/projects')
        # if fzf is installed use it to select a project
        if len(projects) > 0:
            selected_project = iterfzf([f"{project['id']} - {project['name']}" for project in projects], multi=False, prompt="Select a project: ")
            if selected_project is not None:
                project_id = selected_project.split()[0]
            set_config('project', project_id)
            click.echo(f"Selected project: {project_id}")
        else:
            click.Abort("No projects found.")
    else: 
        r = kimai_request('api/projects/' + str(project_id))
        set_config('project', project_id)
        click.echo(f"Selected project: {r['name']}")