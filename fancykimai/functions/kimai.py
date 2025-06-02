import requests
import keyring
import urllib
from fancykimai.functions.config import get_config, get_current_context


def get_context(context_name: str) -> dict[str, str | None]:
    keyring_url = keyring.get_password(f"kimai:{context_name}", "url")
    if keyring_url is None:
        raise ValueError("Context not found: URL is required")

    keyring_api_key = keyring.get_password(f"kimai:{context_name}", "api_key")

    keyring_user = keyring.get_password(f"kimai:{context_name}", "user")
    keyring_password = keyring.get_password(f"kimai:{context_name}", "password")

    has_api_key_auth = keyring_api_key is not None
    has_user_pass_auth = keyring_user is not None and keyring_password is not None

    if not (has_api_key_auth or has_user_pass_auth):
        raise ValueError(
            "Context not found: Either API key or username/password is required"
        )

    return {
        "url": keyring_url,
        "user": keyring_user,
        "password": keyring_password,
        "api_key": keyring_api_key,
    }


def kimai_request(
    path,
    method="GET",
    data=None,
    headers=None,
    base_url="default",
    context_name="default",
) -> dict | None:
    # check if keyring is set
    try:
        selected_context = get_current_context()
        if selected_context is not None:
            context_name = selected_context
        context_values = get_context(context_name)
    except ValueError:
        context_values = {}
    if path != "api/ping":
        has_user_auth = (
            context_values.get("user") is not None
            and context_values.get("password") is not None
        )
        has_api_key_auth = context_values.get("api_key") is not None

        if not (has_user_auth or has_api_key_auth):
            print(
                'Authentication not set. Use "kimai login" to set your authentication. '
                "Either username/password or API key is required."
            )
            return None
    if base_url == "default":
        if context_values.get("url") is None:
            print('Kimai URL not set. Use "kimai login" to set your authentication.')
            return None
        base_url = context_values.get("url")
    url = urllib.parse.urljoin(base_url, path)
    if headers is None:
        headers = {"Content-Type": "application/json"}
    if path != "api/ping":
        api_key = context_values.get("api_key", None)
        if api_key is not None:
            headers["Authorization"] = f"Bearer {api_key}"
        else:
            headers["X-AUTH-USER"] = context_values.get("user")
            headers["X-AUTH-TOKEN"] = context_values.get("password")
    if method.upper() == "GET":
        if data is not None:
            r = requests.get(url, headers=headers, params=data)
        else:
            r = requests.get(url, headers=headers)
    elif method.upper() == "POST":
        r = requests.post(url, headers=headers, json=data)
    elif method.upper() == "PUT":
        r = requests.put(url, headers=headers, json=data)
    elif method.upper() == "DELETE":
        r = requests.delete(url, headers=headers)
        if r.status_code == 204:
            return {"status": "success", "message": "Deleted"}
    else:
        print("Method not supported")
        return None
    r.raise_for_status()

    return r.json()
