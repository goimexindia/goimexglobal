import git
from git import GitCommandError

from hierarchy.loader import RepoToClone
from hierarchy.utils import display


def clone_all(repo_hierarchy: [RepoToClone]):
    for repo in repo_hierarchy:
        display(f"Cloning '{repo.url}' in '{repo.path}'")

        try:
            git.Repo.clone_from(url=repo.url, to_path=repo.path)
        except GitCommandError as e:
            display(f"Error while cloning '{repo.path}'", variant='ERROR', reason=e)

        display('')
