#!/usr/bin/env python

import argparse
import os
import re
from collections import defaultdict

import pkg_resources


def format_file(py_file):
    # remove head and tail blanks, convert ' to "
    content = []
    with open(py_file, 'r') as f:
        for line in f:
            content.append(line.strip().replace('\'', '"'))

    # remove imports in comments; convert multi-line imports to one-line ones
    text = re.sub('""".*?"""|\\\\\n|\(\n|\(|\)', '', '\n'.join(content), 0, re.DOTALL)
    text = re.sub(',\n', ',', text).split('\n')
    return text


def get_packages_from_py_file(py_file):
    text = format_file(py_file)
    packages = set()
    for line in text:
        line = line.strip()
        if line.startswith('import'):
            con = line.strip().split(None, 1)
            if len(con) != 2:
                continue
            imports = con[1].split(',')
            for im in imports:
                im = im.strip()
                if im:
                    packages.add(im.split(None, 1)[0].split('.', 1)[0])
        elif line.startswith('from') and 'import' in line:
            con = line.split()
            if len(con) < 3:
                continue
            if con[2] == 'import':
                im = con[1].strip()
                if im:
                    packages.add(im.split(None, 1)[0].split('.', 1)[0])

    return packages


def get_packages(package_path):
    packages = set()
    for dirpath, dirnames, filenames in os.walk(package_path):
        for fn in filenames:
            if fn.endswith('.py'):
                tmp_packages = get_packages_from_py_file(os.path.join(dirpath, fn))
                packages |= tmp_packages
    return packages


def get_package_projectname(add_version=True):
    package_projectname = defaultdict(list)
    for p in pkg_resources.working_set:
        pv = p.project_name
        if add_version:
            pv += '==' + p.version
        try:
            packages = pkg_resources.get_distribution(p.project_name)._get_metadata('top_level.txt')
            for m in packages:
                package_projectname[m].append(pv)
        except Exception:
            pass
    return package_projectname


def gen_requirements(package_path, add_version=True, abnormal_threshold=2):
    packages = get_packages(package_path)
    package_projectname = get_package_projectname(add_version)

    normal_req = set()
    abnormal_req = set()

    for m in packages:
        if m in package_projectname:
            project_names = package_projectname[m]
            if len(project_names) < abnormal_threshold:
                normal_req |= set(project_names)
            else:
                project_names = ['%s  # for package: %s' % (p, m) for p in project_names]
                abnormal_req |= set(project_names)

    normal_req = sorted(list(normal_req))
    abnormal_req = sorted(list(abnormal_req))

    for req in normal_req:
        print(req)
    if len(abnormal_req) > 0:
        print('# Below are unsure project names (manual check needed): ')
        for req in abnormal_req:
            print(req)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--package_dir', type=str, help='your package path', default='.')
    parser.add_argument('-v', '--add_version', type=int, help='add version (1) or not (0)',
                        choices=(0, 1), default=1)
    args = parser.parse_args()
    add_version = True
    if args.add_version == 0:
        add_version = False
    gen_requirements(args.package_dir, add_version)


if __name__ == '__main__':
    main()
