import click
from fancykimai.functions.contexts import get_contexts
from fancykimai.functions.config import set_config, set_context
from rich import table, console
import json
from iterfzf import iterfzf
from fancykimai.classes.click_groups import AliasedGroup


@click.group(name="contexts", cls=AliasedGroup)
def contexts_group():
    """
    Contexts commands
    """
    pass


@contexts_group.command(name="list")
@click.option(
    "-o",
    "--output",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format",
)
def list_contexts(output: str) -> None:
    """
    List contexts
    """
    contexts = get_contexts()
    if contexts is None:
        click.echo(
            "Please authenticate first and set your context values in the authentication."
        )
        return
    if output == "table":
        columns = [
            {"column": "NAME", "response_key": "name", "function": str},
            {
                "column": "PROJECT_ID",
                "response_key": "project",
                "function": str,
            },
            {"column": "ACTIVITY_ID", "response_key": "activity", "function": str},
        ]
        rich_table = table.Table(title="Contexts")
        for column in columns:
            if column.get("style"):
                rich_table.add_column(column["column"], style=column["style"])
            else:
                rich_table.add_column(column["column"])
        for context in contexts:
            rich_table.add_row(
                *[
                    column["function"](
                        context.get(column.get("response_key", None), None)
                    )
                    for column in columns
                ]
            )
        rich_console = console.Console()
        rich_console.print(rich_table)
    else:
        click.echo(json.dumps(contexts))


@contexts_group.command(name="select")
@click.argument("context_id", type=str, required=False)
def select_project(context_id: str | None = None) -> None:
    """
    Select a context
    """
    contexts = get_contexts()
    if contexts is None:
        click.Abort("Please login first")
        return
    if context_id is None:
        # Get All Contexts
        if contexts is None:
            click.echo(
                "Please authenticate first and set your context values in the authentication."
            )
            return
        # if fzf is installed use it to select a context
        if len(contexts) > 0:
            selected_context = iterfzf(
                [f"{context['name']}" for context in contexts],
                multi=False,
                prompt="Select a context: ",
            )
            if selected_context is not None:
                set_context(selected_context)
                click.echo(f"Selected context: {selected_context}")
        else:
            click.Abort("No contexts found.")
    else:
        if context_id not in [context["name"] for context in contexts]:
            print(f"Context '{context_id}' not found! Please create it first")
            return
        print(f"Selecting {context_id}")
        set_context(context_id)
        click.echo(f"Selected context: {context_id}")


@contexts_group.command(name="create")
@click.option(
    "--name",
    "-n",
    type=str,
    required=True,
    prompt="Name of the context to be created: ",
)
@click.option("--select", is_flag=True)
def create_context(name: str, select: bool) -> None:
    """
    Create a context
    """
    contexts = get_contexts()
    if contexts is None:
        set_config("name", name, context=name)
        print(f"Context '{name}' created successfully.")
        return

    if name in [context["name"] for context in contexts]:
        print(f"Context '{name}' already exists!")
        return

    set_config("name", name, context=name)
    print(f"Context '{name}' created successfully.")
    return

