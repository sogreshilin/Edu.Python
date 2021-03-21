import sys


class Reader:
    def __init__(self, file):
        self._block_size = 512
        self._file = file
        self._data = self._file.read(self._block_size)
        self._size = len(self._data)
        self._eof = self._size < self._block_size
        self._curr = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._curr == self._size and self._eof:
            raise StopIteration()

        rv = self._data[self._curr]
        self._curr += 1

        if self._curr == self._size:
            self._curr = 0
            self._data = self._file.read(self._block_size)
            self._size = len(self._data)
            self._eof = self._size < self._block_size

        return rv


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No filename provided", file=sys.stderr)
        sys.exit(-1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            for symbol in Reader(file):
                print(symbol, end="")

    except Exception as e:
        print(e, file=sys.stderr)

