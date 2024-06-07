import os
import json

def get_config(key) -> str:
    config_file = os.path.expanduser(f"~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
        # Get the selected context
        context = configuration.get("selected_context", "default")
        context_config = next((c for c in configuration["contexts"] if c["name"] == context), None)
        if context_config:
            return context_config.get(key, None)
        else:
            return None
    else:
        return None

def set_config(key: str, value: str, context: str = None):
    config_file = os.path.expanduser(f"~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
        if not context:
            context = configuration.get("selected_context", "default")
        context_config = next((c for c in configuration["contexts"] if c["name"] == context), None)
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
            "selected_context": "default",
            "contexts": [{"name": "default", key: value}]
        }
        with open(config_file, "w") as f:
            f.write(json.dumps(configuration, indent=4))

def unset_config(key: str, context: str = None):
    config_file = os.path.expanduser(f"~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
        if not context:
            context = configuration.get("selected_context", "default")
        context_config = next((c for c in configuration["contexts"] if c["name"] == context), None)
        if context_config:
            context_config.pop(key, None)
            with open(config_file, "w") as f:
                f.write(json.dumps(configuration, indent=4))
        else:
            raise ValueError("Context not found")
    else:
        raise ValueError("Configuration file not found")