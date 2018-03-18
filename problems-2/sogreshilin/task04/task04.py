import sys


def next_bite(file, size=1024):
    while True:
        data = file.read(size)
        if not data:
            break
        for bite in data:
            yield bite


def count_bites(filename):
    counter = 0
    bites_count = dict.fromkeys(range(128, 256), 0)

    with open(filename, 'rb') as file:
        for bite in next_bite(file):
            if bite >= 128:
                counter += 1
                bites_count[bite] += 1

    return counter, bites_count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Expected file name as a command line argument. '
              'File name was not found', file=sys.stderr)
        sys.exit(-1)

    try:
        counter, bites_count = count_bites(sys.argv[1])
        for key, value in sorted(bites_count.items(), key=lambda element: (-element[1], element[0])):
            print("'{}'[{}] - {:.4f}".format(bytes([key]).decode('koi8-r'), key, value / counter))

    except Exception as e:
        print(e, file=sys.stderr)
