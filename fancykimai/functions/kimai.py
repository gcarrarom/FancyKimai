import requests
import keyring
import urllib

def kimai_request(path, method='GET', data=None, headers=None, base_url='default') -> dict:
    # check if keyring is set
    keyring_user = keyring.get_password('kimai', 'user')
    # if keyring is not set and the call doesn't come from kimai_login, return an error
    if keyring_user is None and path != 'api/ping':
        raise ValueError('Authentication not set. Use "kimai login" to set your authentication.')
    keyring_password = keyring.get_password('kimai', 'password')
    keyring_url = keyring.get_password('kimai', 'url')
    if base_url == 'default':
        if keyring_url is None:
            raise ValueError('Kimai URL not set. Use "kimai login" to set your authentication.')
        base_url = keyring_url
    url = urllib.parse.urljoin(base_url, path)
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    if path != 'api/ping':
        headers['X-AUTH-USER'] = keyring_user
        headers['X-AUTH-TOKEN'] = keyring_password
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

