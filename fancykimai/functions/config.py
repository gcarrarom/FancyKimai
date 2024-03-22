import os
import json

def get_config(key) -> str:
    config_file = os.path.expanduser("~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
        return configuration.get(key, None)
    else:
        return None

def set_config(key: str, value: str):
    config_file = os.path.expanduser("~/.config/fancykimai/config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            configuration = json.loads(f.read())
        configuration[key] = value
        with open(config_file, "w") as f:
            f.write(json.dumps(configuration, indent=4))
    else:
        # check if the directory exists
        config_dir = os.path.dirname(config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(config_file, "w") as f:
            f.write(json.dumps({key: value}, indent=4))