from .login import kimai_login
from .projects import projects_group
from .activities import activities_group
from .customers import customers_group
from .teams import teams_group
from .timesheets import timesheets_group
from .config import config_group

commands = [
    kimai_login,
    projects_group,
    activities_group,
    customers_group,
    teams_group,
    timesheets_group,
    config_group,
]