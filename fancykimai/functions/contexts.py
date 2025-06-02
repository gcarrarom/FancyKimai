import keyring

from fancykimai.functions.config import get_config_file


def set_context_in_keyring(
    context_name: str, user: str, api_key: str, url: str, old: bool
):
    if old:
        keyring.set_password(f"kimai:{context_name}", "user", user)
        keyring.set_password(f"kimai:{context_name}", "password", api_key)
    else:
        keyring.set_password(f"kimai:{context_name}", "api_key", api_key)
    keyring.set_password(f"kimai:{context_name}", "url", url)


def get_contexts() -> list[dict[str, str]] | None:
    configuration = get_config_file()
    if configuration is None:
        return None

    contexts = configuration.get("contexts", [])
    if type(contexts) is not list:
        return None

    return contexts
