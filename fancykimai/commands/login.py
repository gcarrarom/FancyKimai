import click
import keyring
from fancykimai.functions.kimai import kimai_request
from fancykimai.functions.config import set_config

def set_context(context_name: str, user: str, api_key: str, url: str):
    keyring.set_password(f'kimai:{context_name}', 'user', user)
    keyring.set_password(f'kimai:{context_name}', 'password', api_key)
    keyring.set_password(f'kimai:{context_name}', 'url', url)

@click.command(name='login')
@click.option('-u', '--user', prompt='Your Kimai username', help='Your Kimai username')
@click.option('-p', '--api-key', prompt='Your Kimai API secret', help='Your API secret', hide_input=True)
@click.option('-k', '--url', prompt='Your Kimai URL', help='Your Kimai URL')
@click.option('-c', '--context-name', default='default', help='The context name to use for this authentication')
def kimai_login(user, api_key, url, context_name):
    # check if the authentication works
    r = kimai_request('api/ping', base_url=url, headers={'X-AUTH-USER': user, 'X-AUTH-TOKEN': api_key})
    if r['message'] != 'pong':
        raise ValueError('Authentication failed')
    # set the user and password in the keyring
    set_context(context_name, user, api_key, url)
    set_config('context', context_name)
    click.echo('Authentication successful')
