import click
import keyring
from fancykimai.functions.kimai import kimai_request

@click.command(name='login')
@click.option('-u', '--user', prompt='Your Kimai username', help='Your Kimai username')
@click.option('-p', '--api-key', prompt='Your Kimai API secret', help='Your API secret', hide_input=True)
@click.option('-k', '--url', prompt='Your Kimai URL', help='Your Kimai URL')
def kimai_login(user, api_key, url):
    # check if the authentication works
    r = kimai_request('api/ping', base_url=url, headers={'X-AUTH-USER': user, 'X-AUTH-TOKEN': api_key})
    if r['message'] != 'pong':
        raise ValueError('Authentication failed')
    # set the user and password in the keyring
    keyring.set_password('kimai', 'user', user)
    keyring.set_password('kimai', 'password', api_key)
    keyring.set_password('kimai', 'url', url)
    click.echo('Authentication successful')
