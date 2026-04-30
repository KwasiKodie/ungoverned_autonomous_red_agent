from openai import OpenAI
import os
from dotenv import load_dotenv

import json

load_dotenv()

url_json = os.getenv("URL_JSON_PATH")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_url_by_key(key, json_path=url_json):
    """
    Returns the URL associated with a given key from a JSON file.

    Args:
        key (str): The key to look up (e.g., "kath")
        json_path (str): Path to the JSON file

    Returns:
        str: URL if found
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} not found")

    with open(json_path, "r") as f:
        data = json.load(f)

    if key not in data:
        raise KeyError(f"Key '{key}' not found in JSON")

    return data[key]

def parse_list(value):
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]
