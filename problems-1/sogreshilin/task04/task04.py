import sys
import os
from os.path import isfile, isdir, join


def ls_size_sorted(dir_path):
    if not isdir(dir_path):
        raise ValueError(dir_path + " is not a directory")

    sizeof_files = {}

    for entry in os.listdir(dir_path):
        path_to_file = join(dir_path, entry)
        if isfile(path_to_file):
            file_info = os.stat(path_to_file)
            sizeof_files[entry] = file_info.st_size

    return sorted(sizeof_files.keys(), key=sizeof_files.get, reverse=True)


def main():
    if len(sys.argv) < 2:
        raise ValueError("Directory name was not found")

    print(*ls_size_sorted(sys.argv[1]), sep="\n")


if __name__ == "__main__":
    main()
