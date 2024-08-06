import os
from git import Repo, Tuple

REPO_DIR = "repo"


def get_latest_commit_sha(repo_url: str, branch: str) -> Tuple[str, str]:
    if repo_url.endswith("/"):
        repo_url = repo_url[:-1]
    project_name = repo_url.split("/")[-1].split(".")[0]
    repo_path = f"{REPO_DIR}/{project_name}"
    if not os.path.exists(repo_path):
        repo = Repo.clone_from(
            url=repo_url,
            to_path=repo_path,
            branch=branch,
        )
    else:
        repo = Repo(repo_path)

    repo.git.checkout(branch)
    remote = repo.remotes.origin
    remote.pull()
    sha = repo.head.object.hexsha

    return repo_path, sha
