import sys
import os
from os.path import isfile, isdir, join


def ls_size_sorted(dir_path):
    file_sizes = list()

    for entry in os.listdir(dir_path):
        path_to_file = join(dir_path, entry)
        if isfile(path_to_file):
            file_info = os.stat(path_to_file)
            file_sizes.append((entry, file_info.st_size))

    return sorted(file_sizes, key=lambda element: (-element[1], element[0]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Directory name was not found", file=sys.stderr)
        sys.exit(-1)

    dir_path = sys.argv[1]
    max_filename_len = 20

    try:
        for filename, size in ls_size_sorted(dir_path):
            print(filename.ljust(max_filename_len)[:max_filename_len], size)

    except Exception as exception:
        print(exception, file=sys.stderr)
        sys.exit(-1)

    sys.exit(0)
