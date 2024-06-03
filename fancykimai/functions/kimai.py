import requests
import keyring
import urllib

def get_context(context_name: str) -> dict:
    keyring_user = keyring.get_password(f'kimai:{context_name}', 'user')
    keyring_password = keyring.get_password(f'kimai:{context_name}', 'password')
    keyring_url = keyring.get_password(f'kimai:{context_name}', 'url')
    if keyring_user is None or keyring_password is None or keyring_url is None:
        raise ValueError('Context not found')
    return {'user': keyring_user, 'password': keyring_password, 'url': keyring_url}

def kimai_request(path, method='GET', data=None, headers=None, base_url='default', context_name='default') -> dict:
    # check if keyring is set
    try:
        context_values = get_context(context_name)
    except ValueError:
        context_values = {}
    # if keyring is not set and the call doesn't come from kimai_login, return an error
    if context_values.get('user') is None and path != 'api/ping':
        raise ValueError('Authentication not set. Use "kimai login" to set your authentication.')
    if base_url == 'default':
        if context_values.get('url') is None:
            raise ValueError('Kimai URL not set. Use "kimai login" to set your authentication.')
        base_url = context_values.get('url')
    url = urllib.parse.urljoin(base_url, path)
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    if path != 'api/ping':
        headers['X-AUTH-USER'] = context_values.get('user')
        headers['X-AUTH-TOKEN'] = context_values.get('password')
    if method.upper() == 'GET':
        if data is not None:
            r = requests.get(url, headers=headers, params=data)
        else:
            r = requests.get(url, headers=headers)
    elif method.upper() == 'POST':
        r = requests.post(url, headers=headers, json=data)
    elif method.upper() == 'PUT':
        r = requests.put(url, headers=headers, json=data)
    elif method.upper() == 'DELETE':
        r = requests.delete(url, headers=headers)
        if r.status_code == 204:
            return {'status': 'success', 'message': 'Deleted'}
    else:
        raise ValueError('Method not supported')
    r.raise_for_status()

    return r.json()

