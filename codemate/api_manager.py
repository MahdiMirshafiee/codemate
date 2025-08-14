import os
import json
from rich import print
import shutil

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".codemate")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

def ensure_config_dir():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

def set_api_key(api_token):
    ensure_config_dir()
    data = {"OPENROUTER_API_KEY": api_token.strip()}
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f)

def get_api_key():
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data.get("OPENROUTER_API_KEY")

def delete_config():
    if os.path.exists(CONFIG_DIR) and os.path.isdir(CONFIG_DIR):
        shutil.rmtree(CONFIG_DIR)
        print("[bold dark_green][!] Codemate config directory deleted successfully.")
    else:
        print("[bold dark_red][!] No Codemate config directory found to delete.")