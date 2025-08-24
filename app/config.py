import os, yaml
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENTS_DIR = os.path.join(BASE_DIR, "clients")

def load_client_config(client_key: str):
    path = os.path.join(CLIENTS_DIR, f"{client_key}.yaml")
    if not os.path.exists(path):
        path = os.path.join(CLIENTS_DIR, "default.yaml")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)