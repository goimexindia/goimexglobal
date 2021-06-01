import os
from pathlib import Path

import yaml


class RepoToClone:
    url: str
    path: Path
    name: str

    def __init__(self, url: str, root_path: Path, name: str = None):
        self.url = url
        if not name:
            name = self._extract_name_from_url()
        self.path = root_path / name

    def _extract_name_from_url(self):
        return self.url.split('/')[-1].replace('.git', '')

    def __repr__(self) -> str:
        return f'<url: {self.url} | path: {self.path}>'

    def __eq__(self, other):
        return self.url == other.url and self.path == other.path


def load_from_file(hierarchy_file: Path):
    if not hierarchy_file.exists():
        raise ValueError(f'File {hierarchy_file} does not exist!')

    hierarchy_yaml = yaml.safe_load(hierarchy_file.read_text())

    _validate(hierarchy_yaml)

    hierarchy = []
    for repo_yaml in hierarchy_yaml['repos']:
        path = Path(os.path.expanduser(repo_yaml['path']))
        repo_to_clone = RepoToClone(repo_yaml['url'], path, repo_yaml.get('name'))
        hierarchy.append(repo_to_clone)

    return hierarchy


def _validate(hierarchy_yaml):
    def raise_error():
        raise ValueError('Invalid Hierarchy. Please check Hierarchy file!')

    if not hierarchy_yaml:
        raise_error()
    if 'repos' not in hierarchy_yaml:
        raise_error()

    for repo_yaml in hierarchy_yaml['repos']:
        if 'url' not in repo_yaml or 'path' not in repo_yaml:
            raise_error()
