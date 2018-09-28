#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Utils for operating files."""

import os
import glob

def _should_pass(path, exclusive_paths):
    if exclusive_paths is None:
        return True

    for exclusive_path in exclusive_paths:
        if exclusive_path in path:
            return False
    else:
        return True


def _is_one_of_name(path, names):
    if names is None:
        return True

    for name in names:
        if name in os.path.basename(path):
            return True
    else:
        return False


def _is_one_of_type(path, types):
    if types is None:
        return True

    for file_type in types:
        if path.endswith('.' + file_type):
            return True
    else:
        return False


def file_name(path):
    """Get the file name without directory and file type."""
    return os.path.basename(path).split('.')[0]


def get_size(path):
    """
    Get size of a file or directory.

    Returns the size in 'kb'.
    """
    total_size = 0
    for directory_path, directory_name, file_names in os.walk(path):
        for name in file_names:
            file_path = os.path.join(directory_path, name)
            total_size += os.path.getsize(file_path)
    return total_size / 1024


def get_paths(root_path, names=None, types=None, exclusive_paths=None):
    """"
    Get all file and directory paths recursively.

    Returns a list of filtered paths.

    :param str start_path: root path which starts searching
    :param list types: file types to filter
    :param list exclusive_paths: directory path that should exclusive
    """
    return [path
            for path in glob.glob(root_path + '/**/*', recursive=True)
            if _is_one_of_name(path, names)
            and _is_one_of_type(path, types)
            and _should_pass(path, exclusive_paths)]


def file_contains(path, string):
    with open(path, 'r') as source_file:
        for line in source_file:
            if line.find(string) != -1:
                return True
        else:
            return False

def fileLine_containStartWith(path, string):
    with open(path, 'r') as source_file:
        for line in source_file:
            if line.find(string) == 0:
                return line
        else:
            return ""
