import os
import json
from typing import Optional


def get_repo_dir() -> str:
    """
    Get the directory path for storing static files in the library.

    Returns:
        str: The target directory path.
    """
    library_dir = os.path.dirname(__file__)
    return os.path.join(library_dir, "statics")


def load_and_merge_json_files(json_path: str, static_dir: Optional[str] = None):
    """
    Load all JSON files from the specified directory into a single dictionary.

    Args:
    - directory_path (str): Path to the directory containing JSON files.

    Returns:
    - dict: A dictionary where keys are file names (without extension) and values are loaded JSON data.
    """
    planets_data = {}

    source_dir = get_repo_dir()
    if static_dir:
        source_dir = static_dir

    directory_path = os.path.join(get_repo_dir(), json_path)

    # Validate directory path
    if not os.path.isdir(directory_path):
        raise ValueError(f"Directory '{directory_path}' does not exist.")

    # Load JSON files
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="utf8") as f:
                try:
                    json_data = json.load(f)
                    # Remove file extension from filename
                    file_key = os.path.splitext(filename)[0]
                    planets_data[file_key] = json_data
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON from {filename}: {e}")

    return planets_data
