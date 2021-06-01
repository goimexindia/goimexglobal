from hierarchy.cloner import clone_all
from hierarchy.loader import load_from_file


def clone_hierarchy(hierarchy_file):
    clone_all(load_from_file(hierarchy_file))
