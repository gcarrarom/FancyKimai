from fancykimai.functions.kimai import kimai_request
from fancykimai.functions.config import get_config
from iterfzf import iterfzf

def select_project(ctx, param, value: str) -> str:
    '''
    Select a project from the list of projects in Kimai and return the id
    '''
    default = get_config('project')
    projects = kimai_request('api/projects')
    if value:
        # Check if value is in the id or name of the projects
        for project in projects:
            if value == project['id']:
                return project['id']
            if value == project['name']:
                return project['id']
        # If not found, return an error
        raise ValueError('Project not found')
    else:
        # If no value is given, but there's a default project, return the id
        if default:
            return default
        # If no value is given and there's no default project, prompt the user
        project_names = [f"{project['id']} - {project['name']}" for project in projects]
        selected_project = iterfzf(project_names)
        if selected_project:
            return selected_project.split(' - ')[0]
        else:
            raise ValueError('Project not found')