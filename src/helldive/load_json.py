import os
import subprocess


def clone_or_pull_repo(repo_url, target_dir):
    if not os.path.exists(target_dir):
        print(f"Cloning repository from {repo_url} to {target_dir}")
        subprocess.run(["git", "clone", repo_url, target_dir], check=True)
    else:
        print(f"Pulling latest changes in {target_dir}")
        subprocess.run(["git", "-C", target_dir, "pull"], check=True)


def get_repo_dir():
    # Determine the location of the repository
    library_dir = os.path.dirname(__file__)
    return library_dir
    repo_dir = os.path.join(library_dir, "repo_name")
    return repo_dir


if __name__ == "__main__":
    # Example usage
    repo_url = "https://github.com/CrosswaveOmega/json.git"  # Replace with your git repo URL
    target_dir = get_repo_dir() + "/statics"
    clone_or_pull_repo(repo_url, target_dir)
