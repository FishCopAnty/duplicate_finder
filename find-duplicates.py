#!/usr/bin/env python3
import sys
import hashlib
import os
import math
from tempfile import TemporaryDirectory


def list_files(path: str) -> list[str]:
    """
    Recursively lists all file paths in the specified directory.
    """
    files = []
    for root, _, filenames in os.walk(path):
        for name in filenames:
            files.append(os.path.join(root, name))
    return files


def get_file_size(file_path: str) -> int:
    """
    Retrieves the size of the specified file in bytes.
    """
    try:
        return os.path.getsize(file_path)
    except OSError:
        return None


def hash_first_1k_bytes(file_path: str) -> str:
    """
    Computes the SHA-1 hash of the first 1024 bytes of a file.
    """
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        sha1.update(f.read(1024))
    return sha1.hexdigest()


def hash_file(file_path: str) -> str:
    """
    Computes the SHA-1 hash of the entire file.
    """
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha1.update(chunk)
    return sha1.hexdigest()


def filter_files_by_size(file_paths: list[str]) -> list[str]:
    """
    Filters a list of files, grouping them by size and identifying potential duplicates.
    """
    files_by_size = {}
    for file_path in file_paths:
        file_size = get_file_size(file_path)
        if file_size:
            files_by_size.setdefault(file_size, []).append(file_path)

    duplicates = []
    for paths in files_by_size.values():
        if len(paths) > 1:
            duplicates.extend(paths)
    return duplicates


def filter_files_by_first_1k_bytes(file_paths: list[str]) -> list[str]:
    """
    Filters a list of files, grouping them by the hash of their first 1024 bytes.
    """
    files_by_hash = {}
    for file_path in file_paths:
        h = hash_first_1k_bytes(file_path)
        files_by_hash.setdefault(h, []).append(file_path)

    duplicates = []
    for paths in files_by_hash.values():
        if len(paths) > 1:
            duplicates.extend(paths)
    return duplicates


def group_files_by_full_hash(file_paths: list[str]) -> list[list[str]]:
    """
    Groups files by their full content hash and identifies duplicate groups.
    """
    files_by_hash = {}
    for file_path in file_paths:
        h = hash_file(file_path)
        files_by_hash.setdefault(h, []).append(file_path)

    return [paths for paths in files_by_hash.values() if len(paths) > 1]


def file_size_string(num_bytes: int) -> str:
    """
    Returns a number of bytes in a human-readable format using base 1000.
    """
    sizes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    if num_bytes < 1000:
        return f"{num_bytes:.2f}B"

    exponent = int(math.log(num_bytes, 1000))
    value = num_bytes / (1000 ** exponent)
    return f"{value:.2f}{sizes[exponent]}"


def print_duplicates(duplicates: list[list[str]]):
    """
    Prints details of duplicate files, including their sizes and paths.
    """
    for files in duplicates:
        print("Found duplicate files:")
        size = get_file_size(files[0])
        print("Size: ", file_size_string(size))
        for file in files:
            print(file)


def check_for_duplicates(paths: list[str]):
    """
    Checks for duplicate files in the given paths and prints the results.
    """
    files = []
    for path in paths:
        files.extend(list_files(path))
    files = filter_files_by_size(files)
    files = filter_files_by_first_1k_bytes(files)
    duplicates = group_files_by_full_hash(files)
    print_duplicates(duplicates)


def main():
    """
    The main entry point of the script.
    """
    if len(sys.argv) < 2:
        print("Usage: find_duplicates.py <path> [<path> ...]")
        sys.exit(1)
    check_for_duplicates(sys.argv[1:])


if __name__ == "__main__":
    main()
