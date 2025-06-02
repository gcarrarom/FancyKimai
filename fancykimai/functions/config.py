import os
import json


def get_config_file() -> dict[str, str | list[dict[str, str]]] | None:
    config_file = os.path.expanduser("~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
            return configuration

    pass


def get_current_context() -> str | None:
    config_file = os.path.expanduser("~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
        return configuration.get("selected_context", None)
    else:
        return None


def get_config(key: str) -> str | None:
    config_file = os.path.expanduser("~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
        # Get the selected context
        context = configuration.get("selected_context", "default")
        context_config = next(
            (c for c in configuration["contexts"] if c["name"] == context), None
        )
        if context_config:
            return context_config.get(key, None)
        else:
            return None
    else:
        return None


def set_context(context: str) -> bool:
    config_file = os.path.expanduser("~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
        contexts = configuration.get("contexts", [])
        if context in [context.get("name") for context in contexts]:
            configuration["selected_context"] = context
        else:
            return False
        with open(config_file, "w") as f:
            f.write(json.dumps(configuration, indent=4))
            return True
    return False


def set_config(key: str, value: str, context: str | None = None):
    config_file = os.path.expanduser("~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
        if not context:
            context = configuration.get("selected_context", "default")
        context_config = next(
            (c for c in configuration["contexts"] if c["name"] == context), None
        )
        if context_config:
            context_config[key] = value
        else:
            configuration["contexts"].append({"name": context, key: value})
        with open(config_file, "w") as f:
            f.write(json.dumps(configuration, indent=4))
    else:
        config_dir = os.path.dirname(config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        configuration = {
            "selected_context": "default" if context is None else context,
            "contexts": [
                {"name": "default" if context is None else context, key: value}
            ],
        }
        with open(config_file, "w") as f:
            f.write(json.dumps(configuration, indent=4))


def unset_config(key: str, context: str | None = None):
    config_file = os.path.expanduser("~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
        if not context:
            context = configuration.get("selected_context", "default")
        context_config = next(
            (c for c in configuration["contexts"] if c["name"] == context), None
        )
        if context_config:
            context_config.pop(key, None)
            with open(config_file, "w") as f:
                f.write(json.dumps(configuration, indent=4))
        else:
            raise ValueError("Context not found")
    else:
        raise ValueError("Configuration file not found")
