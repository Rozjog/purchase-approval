import json


def load_data(filename: str):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []


def save_data(filename: str, requests: list):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(requests, file, ensure_ascii=False, indent=4)
