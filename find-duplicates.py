#!/usr/bin/env python3
import sys
import hashlib
import os
import math
from tempfile import TemporaryDirectory


def list_files(path: str) -> list[str]:
    """
    Recursively lists all file paths in the specified directory.

    Args:
        path (str): The root directory to search for files.

    Returns:
        list[str]: A list of file paths found in the directory and its subdirectories.
    """
    # Run "pytest find_duplicates.py -k list_files" to test your implementation
    raise NotImplementedError()


def get_file_size(file_path: str) -> int:
    """
    Retrieves the size of the specified file in bytes.

    Args:
        file_path (str): The path to the file.

    Returns:
        int or None: The file size in bytes, or None if the file cannot be accessed.
    """
    # Run "pytest find_duplicates.py -k get_file_size" to test your implementation
    raise NotImplementedError()


def hash_first_1k_bytes(file_path: str) -> str:
    """
    Computes the SHA-1 hash of the first 1024 bytes of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The hexadecimal SHA-1 hash of the first 1024 bytes of the file.
    """
    # Run "pytest find_duplicates.py -k hash_first_1k_bytes" to test your implementation
    raise NotImplementedError()


def hash_file(file_path: str) -> str:
    """
    Computes the SHA-1 hash of the entire file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The hexadecimal SHA-1 hash of the file.
    """
    # Run "pytest find_duplicates.py -k hash_file" to test your implementation
    raise NotImplementedError()


def filter_files_by_size(file_paths: list[str]) -> list[str]:
    """
    Filters a list of files, grouping them by size and identifying potential duplicates.

    Args:
        file_paths (list[str]): A list of file paths to analyze.

    Returns:
        list[str]: A list of file paths that have duplicates based on file size.
    """
    files_by_size = {}
    for file_path in file_paths:
        file_size = get_file_size(file_path)
        if file_size:
            if file_size in files_by_size:
                files_by_size[file_size].append(file_path)
            else:
                files_by_size[file_size] = [file_path]
    duplicates = []
    for paths in files_by_size.values():
        if len(paths) <= 1:
            continue
        duplicates.extend(paths)
    return duplicates


def filter_files_by_first_1k_bytes(file_paths: list[str]) -> list[str]:
    """
    Filters a list of files, grouping them by the hash of their first 1024 bytes.

    Args:
        file_paths (list[str]): A list of file paths to analyze.

    Returns:
        list[str]: A list of file paths that have duplicates based on the hash of the first 1024 bytes.
    """
    files_by_hash = {}
    for file_path in file_paths:
        hash = hash_first_1k_bytes(file_path)
        if hash in files_by_hash:
            files_by_hash[hash].append(file_path)
        else:
            files_by_hash[hash] = [file_path]
    duplicates = []
    for paths in files_by_hash.values():
        if len(paths) <= 1:
            continue
        duplicates.extend(paths)
    return duplicates


def group_files_by_full_hash(file_paths: list[str]) -> list[list[str]]:
    """
    Groups files by their full content hash and identifies duplicate groups.

    Args:
        file_paths (list[str]): A list of file paths to analyze.

    Returns:
        list[list[str]]: A list of groups where each group contains file paths of identical files.
    """
    files_by_hash = {}
    for file_path in file_paths:
        hash = hash_file(file_path)
        if hash in files_by_hash:
            files_by_hash[hash].append(file_path)
        else:
            files_by_hash[hash] = [file_path]
    duplicates = []
    for hash, paths in files_by_hash.items():
        if len(paths) > 1:
            duplicates.append(paths)
    return duplicates


def file_size_string(num_bytes: int) -> str:
    """
    Returns a number of bytes in a human-readable format (e.g., KB, MB).
    We use powers of 1000 (not 1024) to represent file sizes.
    e.g 1000 -> 1.00KB
        1500000 -> 1.50MB

    Args:
        file_path (str): The path to the file.

    Returns:
        None
    """
    sizes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    # Run "pytest find_duplicates.py -k file_size_string" to test your implementation
    raise NotImplementedError()


def print_duplicates(duplicates: list[list[str]]):
    """
    Prints details of duplicate files, including their sizes and paths.

    Args:
        duplicates (list[list[str]]): A list of duplicate file groups.
                                      Each group contains file paths of identical files.

    Returns:
        None
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

    Args:
        paths (list[str]): A list of directory paths to search for duplicates.

    Returns:
        None
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
    The main entry point of the script. Checks for duplicate files in the directories
    provided as command-line arguments.

    Returns:
        None
    """
    if len(sys.argv) < 2:
        print("Usage: find_duplicates.py <path> [<path> ...]")
        sys.exit(1)
    check_for_duplicates(sys.argv[1:])


if __name__ == "__main__":
    main()


# Pytest Tests
# Use pytest find_duplicates.py to run these tests.


def create_file(directory, name, content):
    """Helper function to create a file with the given content."""
    file_path = os.path.join(directory, name)
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


def test_list_files():
    """Test if list_files correctly lists all files."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        file2 = create_file(temp_dir, "file2.txt", "Hello World")
        file3 = create_file(temp_dir, "file3.txt", "Different Content")

        files = list_files(temp_dir)
        assert set(files) == {file1, file2, file3}


def test_list_files_recursive():
    """Test if list_files correctly lists all files recursively."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        subdir = os.path.join(temp_dir, "subdir")
        os.mkdir(subdir)
        file2 = create_file(subdir, "file2.txt", "Different Content")

        files = list_files(temp_dir)
        assert set(files) == {file1, file2}


def test_get_file_size():
    """Test if get_file_size returns correct file sizes."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        file2 = create_file(temp_dir, "file2.txt", "Different Content")

        assert get_file_size(file1) == len("Hello World")
        assert get_file_size(file2) == len("Different Content")


def test_hash_first_1k_bytes():
    """Test if hash_first_1k_bytes correctly computes the hash of the first 1024 bytes."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        file2 = create_file(temp_dir, "file2.txt", "Hello World")
        file3 = create_file(temp_dir, "file3.txt", "Different Content")
        file4 = create_file(temp_dir, "file4.txt", "A" * 1024 + "B" * 24)
        file5 = create_file(temp_dir, "file5.txt", "A" * 1024 + "C" * 24)

        hash1 = hash_first_1k_bytes(file1)
        hash2 = hash_first_1k_bytes(file2)
        hash3 = hash_first_1k_bytes(file3)
        hash4 = hash_first_1k_bytes(file4)
        hash5 = hash_first_1k_bytes(file5)

        assert hash1 == hash2
        assert hash4 == hash5
        assert hash1 != hash3


def test_hash_file():
    """Test if hash_file computes the correct full file hash."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        file2 = create_file(temp_dir, "file2.txt", "Hello World")
        file3 = create_file(temp_dir, "file3.txt", "Different Content")

        hash1 = hash_file(file1)
        hash2 = hash_file(file2)
        hash3 = hash_file(file3)

        assert hash1 == "0a4d55a8d778e5022fab701977c5d840bbc486d0"
        assert hash1 == hash2
        assert hash1 != hash3


def test_filter_files_by_size():
    """Test if filter_files_by_size identifies files with the same size."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        file2 = create_file(temp_dir, "file2.txt", "Hello World")
        file3 = create_file(temp_dir, "file3.txt", "Different Content")

        duplicates = filter_files_by_size([file1, file2, file3])
        assert set(duplicates) == {file1, file2}


def test_filter_files_by_first_1k_bytes():
    """Test if filter_files_by_first_1k_bytes groups files by the hash of the first 1KB."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        file2 = create_file(temp_dir, "file2.txt", "Hello World")
        file3 = create_file(temp_dir, "file3.txt", "Different Content")
        file4 = create_file(temp_dir, "file4.txt", "A" * 1024 + "B" * 24)
        file5 = create_file(temp_dir, "file5.txt", "A" * 1024 + "C" * 24)

        duplicates = filter_files_by_first_1k_bytes([file1, file2, file3, file4, file5])
        assert set(duplicates) == {file1, file2, file4, file5}


def test_group_files_by_full_hash():
    """Test if group_files_by_full_hash identifies files with identical content."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        file2 = create_file(temp_dir, "file2.txt", "Hello World")
        file3 = create_file(temp_dir, "file3.txt", "Different Content")
        file4 = create_file(temp_dir, "file4.txt", "A" * 1024 + "B" * 24)
        file5 = create_file(temp_dir, "file5.txt", "A" * 1024 + "C" * 24)

        groups = group_files_by_full_hash([file1, file2, file3, file4, file5])

        assert len(groups) == 1  # Only one group of duplicates
        assert set(groups[0]) == {file1, file2}


def test_file_size_string():
    """Test if file_size_string returns human-readable file sizes."""
    assert file_size_string(1) == "1.00B"
    assert file_size_string(999) == "999.00B"
    assert file_size_string(1000) == "1.00KB"
    assert file_size_string(1500000) == "1.50MB"
    assert file_size_string(2000000000) == "2.00GB"
    assert file_size_string(2500000000000) == "2.50TB"
