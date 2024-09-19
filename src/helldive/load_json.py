import os
import httpx
import zipfile
from typing import Optional

"""Attempt to fetch the latest copy of the static JSON files."""


def get_latest_release_zip(repo_owner: str, repo_name: str, zip_file_name: str, target_dir: str) -> None:
    """
    Download the specified zip file from the latest release of the given repository using httpx.

    Args:
        repo_owner (str): The owner of the GitHub repository.
        repo_name (str): The name of the GitHub repository.
        zip_file_name (str): The name of the zip file to download from the latest release.
        target_dir (str): The directory to extract the downloaded zip file.
    """
    releases_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    # Get the latest release metadata
    with httpx.Client() as client:
        response = client.get(releases_url)
        response.raise_for_status()
        latest_release = response.json()

    # Find the asset with the zip file
    asset_url: Optional[str] = None
    for asset in latest_release["assets"]:
        print(asset, asset["name"], zip_file_name)
        if asset["name"] == zip_file_name:
            asset_url = asset["browser_download_url"]
            break

    if not asset_url:
        raise FileNotFoundError(f"{zip_file_name} not found in the latest release.")

    # Download the zip file
    print(f"Downloading {zip_file_name} from the latest release...")
    zip_path = os.path.join(target_dir, zip_file_name)
    with httpx.Client() as client:
        with client.stream("GET", asset_url, follow_redirects=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_bytes():
                    f.write(chunk)

    # Extract the zip file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(target_dir)

    # Optionally, remove the zip file after extraction
    os.remove(zip_path)
    print(f"Extracted {zip_file_name} to {target_dir}.")


def get_repo_dir() -> str:
    """
    Get the directory path for storing static files in the library.

    Returns:
        str: The target directory path.
    """
    library_dir = os.path.dirname(__file__)
    return os.path.join(library_dir, "statics")


def download_latest_static_json():
    repo_owner = "CrosswaveOmega"
    repo_name = "json"
    zip_file_name = "json-files.zip"
    target_dir = get_repo_dir()

    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Download and extract the latest release zip
    get_latest_release_zip(repo_owner, repo_name, zip_file_name, target_dir)


if __name__ == "__main__":
    # Example usage
    download_latest_static_json()
