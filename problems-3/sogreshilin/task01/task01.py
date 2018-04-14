import sys
import re
import math


def collect_data(file):
    sum = 0
    sum_squares = 0
    count = 0

    pattern = re.compile(b'\d+ usec')

    # ignore very first value
    for line in file:
        if line.startswith(b'open'):
            break

    for line in file:
        if line.startswith(b'open'):
            value = int(line.split()[2])
            sum += value
            sum_squares += value * value
            count += 1

    return count, sum, sum_squares


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Path to file was not provided", file=sys.stderr)
        sys.exit(-1)

    filename = sys.argv[1]
    try:
        with open(filename, 'rb') as file:
            count, sum, sum_squares = collect_data(file)

            if count > 0:
                mean = sum / count
                std = (sum_squares - sum * sum / count) / count
                print("mean = {}".format(mean))
                print("std  = {}".format(math.sqrt(std)))

            else:
                print("sample is empty")

    except Exception as e:
        print(e, file=sys.stderr)
