import json
import os

class FileEmptyError(Exception):
    pass

def read_json(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSON file not found: {path}")

    if os.path.getsize(path) == 0:
        raise FileEmptyError(f"JSON file is empty: {path}")

    with open(path, "r") as f:
        return json.load(f)


def write_json(path: str, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    
def read_text(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Text file not found: {path}")

    if os.path.getsize(path) == 0:
        raise FileEmptyError(f"Text file is empty: {path}")

    with open(path, "r") as f:
        return f.read().strip()


def write_text(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)
