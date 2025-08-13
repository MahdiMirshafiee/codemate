import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".codemate")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

def ensure_config_dir():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

def set_api_key(api_key):
    ensure_config_dir()
    data = {"OPENROUTER_API_KEY": api_key.strip()}
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f)
    print("API Key saved successfully.")

def get_api_key():
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data.get("OPENROUTER_API_KEY")