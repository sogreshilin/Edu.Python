


class Vector:
    """Here goes class documentation"""

    def __init__(self, coordinates):
        self._size = len(coordinates)
        self._coordinates = coordinates

    def __str__(self):
        return '({})'.format(', '.join(map(str, self._coordinates)))

    def __len__(self):
        return self._size

    def __getitem__(self, item):
        return self._coordinates[item]

    def __setitem__(self, key, value):
        self._coordinates[key] = value

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError('Vectors have different sizes: {} and {}'
                             .format(len(self), len(other)))

        coordinates = list()
        for i in range(len(self)):
            coordinates.append(self[i] + other[i])

        return Vector(coordinates)

    def __iadd__(self, other):
        if len(self) != len(other):
            raise ValueError('Vectors have different sizes: {} and {}'
                             .format(len(self), len(other)))

        for i in range(len(self)):
            self[i] += other[i]

        return self

    def __neg__(self):
        for i in range(len(self)):
            self[i] = -self[i]




if __name__ == '__main__':
    v1 = Vector([1, 2, 3])
    v2 = Vector([1, 1, 1])
    v2 = -v2;
    print(v2)
    # v2 += v1


