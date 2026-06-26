import json
import os


def load_json(file_path):
    """
    Load a JSON file safely.
    Returns {} if file doesn't exist.
    """

    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, file_path):
    """
    Save dictionary to JSON.
    """

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)