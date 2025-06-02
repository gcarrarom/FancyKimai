import click
from fancykimai.functions.kimai import kimai_request
from fancykimai.functions.config import set_config
from fancykimai.functions.contexts import set_context_in_keyring


@click.command(name="login")
@click.option(
    "-u",
    "--user",
    help="Your Kimai username",
    required=False,
)
@click.option(
    "-p",
    "--api-key",
    prompt="Your Kimai API secret",
    help="Your API secret",
    hide_input=True,
)
@click.option("-k", "--url", prompt="Your Kimai URL", help="Your Kimai URL")
@click.option(
    "-c",
    "--context-name",
    default="default",
    help="The context name to use for this authentication",
)
@click.option(
    "--old",
    is_flag=True,
    help="Whether or not to use the 'old' X-AUTH-USER' authentication method. To be deprecated",
)
def kimai_login(user, api_key, url, context_name, old):
    # check if the authentication works
    if old:
        r = kimai_request(
            "api/ping",
            base_url=url,
            headers={"X-AUTH-USER": user, "X-AUTH-TOKEN": api_key},
        )
        if r["message"] != "pong":
            raise ValueError("Authentication failed")
    else:
        r = kimai_request(
            "api/ping", base_url=url, headers={"Authorization": f"Bearer {api_key}"}
        )
        if r["message"] != "pong":
            raise ValueError("Authentication failed")
    # set the user and password in the keyring
    set_context_in_keyring(context_name, user, api_key, url, old)
    set_config("context", context_name)
    click.echo("Authentication successful")
