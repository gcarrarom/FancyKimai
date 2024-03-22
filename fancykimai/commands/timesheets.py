import click
from fancykimai.functions.kimai import kimai_request
from fancykimai.functions.config import get_config
import rich
from rich import table, console
import datetime
import json
from iterfzf import iterfzf


@click.group(name="timesheets")
def timesheets_group():
    pass


@timesheets_group.command(name="list")
@click.option(
    "-o",
    "--output",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format",
)
@click.option("-a", "--active", help="Only show active timesheets", is_flag=True)
@click.option("-p", "--project", type=int, help="Filter by project ID")
@click.option("-u", "--user", type=int, help="Filter by user ID")
@click.option("-b", "--begin", type=str, help="Filter by begin date")
@click.option("-e", "--end", type=str, help="Filter by end date")
@click.option("--show-costs", help="Show costs", is_flag=True)
@click.option("--show-total", help="Show total", is_flag=True)
def list_timesheets(
    output: str,
    active: bool,
    project: int,
    user: int,
    begin: str,
    end: str,
    show_costs: bool,
    show_total: bool,
):
    # format the begin and end dates
    if begin:
        begin = datetime.datetime.strptime(begin, "%Y-%m-%d").strftime(
            "%Y-%m-%dT00:00:00"
        )
    if end:
        end = datetime.datetime.strptime(end, "%Y-%m-%d").strftime("%Y-%m-%dT23:59:59")
    r = kimai_request(
        "api/timesheets",
        data={
            "project": project,
            "user": user,
            "begin": begin,
            "end": end,
            "active": (1 if active else None),
        },
    )
    if output == "table":
        columns = [
            {"column": "ID", "response_key": "id", "function": str, "style": "cyan"},
            {
                "column": "Activity",
                "response_key": "activity",
                "function": str,
                "style": "magenta",
            },
            {
                "column": "Project",
                "response_key": "project",
                "function": str,
                "style": "green",
            },
            {
                "column": "Start",
                "response_key": "begin",
                "function": lambda date: (
                    datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if date
                    else "Active"
                ),
                "style": "yellow",
            },
            {
                "column": "End",
                "response_key": "end",
                "function": lambda date: date if date else "Active",
                "style": "blue",
            },
            {
                "column": "Duration (Hours)",
                "response_key": "duration",
                "function": lambda s: str(s / 3600),
                "style": "red",
            },
            {
                "column": "User",
                "response_key": "user",
                "function": str,
                "style": "cyan",
            },
            {
                "column": "Description",
                "response_key": "description",
                "function": str,
                "style": "magenta",
            },
        ]
        if show_costs or show_total:
            columns.append(
                {
                    "column": "Cost",
                    "response_key": "rate",
                    "function": lambda s: str(s),
                    "style": "green",
                }
            )
        # define a table using rich to print out the values
        rich_table = table.Table(title="Timesheets")
        totals = {"duration": 0, "rate": 0}
        for column in columns:
            rich_table.add_column(column["column"], style=column["style"])
        for timesheet in r:
            rich_table.add_row(
                *[
                    column["function"](timesheet[column["response_key"]])
                    for column in columns
                ]
            )
            totals["duration"] += float(timesheet["duration"])
            totals["rate"] += float(timesheet["rate"])
        if show_total:
            # add divider for the totals
            rich_table.add_row("", "", "", "", "", "", "", "")
            # add a row for the totals
            rich_table.add_row(
                "Total",
                "",
                "",
                "",
                "",
                str(totals["duration"] / 3600),
                "",
                "",
                str(totals["rate"]),
            )
        rich_console = console.Console()
        rich_console.print(rich_table)
    else:
        click.echo(rich.print(json.dumps(r)))


@timesheets_group.command(name="start")
# get the project option from the configuration file if there's any. Otherwise it's required
@click.option(
    "-p",
    "--project",
    type=int,
    required=True,
    help="Project ID",
    default=get_config("project"),
)
@click.option(
    "-a",
    "--activity",
    type=int,
    required=True,
    help="Activity ID",
    default=get_config("activity"),
)
@click.option("-d", "--description", type=str, required=True, help="Description")
def start_timesheet(project: int, activity: int, description: str):
    """
    Start a new timesheet entry
    """
    begin = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        r = kimai_request(
            "api/timesheets",
            method="post",
            data={
                "project": project,
                "activity": activity,
                "description": description,
                "begin": begin,
            },
        )
        click.echo(f"Started timesheet {r['id']} for project {r['project']} successfully.")
    except Exception as e:
        click.echo(f"Error: {e}")


@timesheets_group.command(name="stop")
@click.option("-i", "--id", type=int, required=True, help="Timesheet ID")
def stop_timesheet(id: int):
    end = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        r = kimai_request(f"api/timesheets/{id}/stop", method="get", data={"end": end})
        click.echo(f"Timesheet {id} stopped successfully.")
    except Exception as e:
        click.echo(f"Error: {e}")


@timesheets_group.command(name="delete")
@click.argument("timesheet_id", type=int, required=False)
def delete_timesheet(timesheet_id: int):
    if timesheet_id is None:
        # get all timesheets
        timesheets = kimai_request("api/timesheets")
        if len(timesheets) > 0:
            selected_timesheet = iterfzf(
                [f"{timesheet['id']} - {timesheet['description']}".replace("\r\n", "") for timesheet in timesheets],
                multi=False,
                prompt="Select a timesheet: ",
            )
            if selected_timesheet:
                timesheet_id = selected_timesheet.split()[0]
            else:
                click.echo("No timesheet selected.")
                raise click.Abort("No timesheet selected.")
        else:
            click.echo("No timesheets found.")
            raise click.Abort("No timesheets found.")
    try:
        r = kimai_request(f"api/timesheets/{timesheet_id}", method="delete")
        click.echo(f"Timesheet {timesheet_id} deleted successfully.")
    except Exception as e:
        click.echo(f"Error: {e}")


@timesheets_group.command(name="set")
@click.option(
    "-p",
    "--project",
    type=int,
    required=True,
    help="Project ID",
    default=get_config("project"),
)
@click.option(
    "-a",
    "--activity",
    type=int,
    required=True,
    help="Activity ID",
    default=get_config("activity"),
)
@click.option("-d", "--description", type=str, required=True, help="Description")
@click.option("-b", "--begin", type=str, required=True, help="Begin date", default=datetime.datetime.now().strftime("%Y-%m-%d"))
@click.option("-e", "--end", type=str, required=False, help="End date")
def set_timesheet(project: int, activity: int, description: str, begin: str, end: str):
    # Check if the hours are set on the dates
    begin_datetime = datetime.datetime.strptime(begin, "%Y-%m-%d")
    if end:
        end_datetime = datetime.datetime.strptime(end, "%Y-%m-%d")
    else:
        end_datetime = begin_datetime
        end = begin
    if begin_datetime > end_datetime:
        click.echo("Begin date cannot be after end date.")
        raise click.Abort("Begin date cannot be after end date.")
    # ask for the time to be set
    begin_time = click.prompt("Begin time", type=str, default="00:00")
    end_time = click.prompt("End time", type=str, default="23:59")
    begin = f"{begin}T{begin_time}:00"
    end = f"{end}T{end_time}:00"
    # Check if the begin and end dates are valid
    begin_datetime = datetime.datetime.strptime(begin, "%Y-%m-%dT%H:%M:%S")
    end_datetime = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
    if begin_datetime > end_datetime:
        click.echo("Begin date cannot be after end date.")
        raise click.Abort("Begin date cannot be after end date.")
    r = kimai_request(
        "api/timesheets",
        method="post",
        data={
            "project": project,
            "activity": activity,
            "description": description,
            "begin": datetime.datetime.strftime(begin_datetime, "%Y-%m-%dT%H:%M:%S"),
            "end": datetime.datetime.strftime(end_datetime, "%Y-%m-%dT%H:%M:%S"),
        },
    )
    click.echo(r)


if __name__ == "__main__":
    delete_timesheet()