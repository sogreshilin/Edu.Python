import heapq
import sys
import math


def _skip_first_occurrence(file, pattern):
    for line in file:
        if line.startswith(pattern):
            break
    return file


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('filename was not provided', file=sys.stderr)
        sys.exit(-1)

    with open(sys.argv[1]) as file:
        count = len([line for line in _skip_first_occurrence(file, 'open') if line.startswith('open')])
        heap_size = int(math.ceil(count / 10))

        heap = [0] * heap_size

        file.seek(0)
        _skip_first_occurrence(file, 'open')

        np_k = 0

        for line in file:
            if not line.startswith('open'):
                continue

            current_value = int(line.split()[2])

            if current_value > heap[0]:
                heapq.heappushpop(heap, current_value)

    print(f'upper decile = {heap[0]}')


