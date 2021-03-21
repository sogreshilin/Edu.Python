import unittest
import types




class Vector:
    """
    Vector class represents one-dimensional mathematical vector.
    Vector has typical for vector operations.

    """
    COORDINATE_TYPES = (int, float, complex)

    def __init__(self, *args):
        """
        Create vector with specified coordinates.
        The size of vector cannot be changed after vector construction.

        :param *args: list or tuple of int, float or complex elements
                      or varargs of int, float or complex elements

        """
        if len(args) == 0:
            self._size = 0
            self._coordinates = []
            return

        if len(args) == 1:
            if Vector._is_iterable(args[0]) and not isinstance(args[0], str):
                raw_coordinates = list(args[0])
            else:
                raw_coordinates = [args[0]]
        else:
            raw_coordinates = [*args]

        raw_coordinates = [self._try_parse(c) for c in raw_coordinates]
        self._size = len(raw_coordinates)
        self._coordinates = self._upgrade_type(raw_coordinates)

    @staticmethod
    def _try_parse(obj):
        if Vector._is_numeric(obj):
            return obj
        return Vector._parse_as(obj, Vector.COORDINATE_TYPES)

    @staticmethod
    def _parse_as(obj, types):
        for type in types:
            try:
                return type(obj)
            except ValueError:
                pass
        raise TypeError('Invalid coordinate type: '
                        'cannot be converted to a number')

    @staticmethod
    def _is_iterable(obj):
        try:
            _ = (element for element in obj)
        except TypeError:
            return False
        else:
            return True

    @staticmethod
    def _is_numeric(obj):
        return isinstance(obj, Vector.COORDINATE_TYPES)

    @staticmethod
    def _max_numeric_type(numbers):
        types = set(map(lambda number: type(number), numbers))
        for coordinate_type in reversed(Vector.COORDINATE_TYPES):
            if coordinate_type in types:
                return coordinate_type
        return None

    @staticmethod
    def _upgrade_type(numbers):
        max_type = Vector._max_numeric_type(numbers)
        return [max_type(element) for element in numbers]

    @classmethod
    def zeros(cls, size):
        """
        Creates vector with all `size` coordinates set to 0

        :param size: int
        :return: Vector

        """
        return Vector([0] * size)

    @classmethod
    def ones(cls, size):
        """
        Creates vector with all `size` coordinates set to 1

        :param size: int
        :return: Vector

        """
        return Vector([1] * size)

    def __str__(self):
        """
        String representation of Vector in format `(c0, c1, ..., cn)`

        :return: str

        """
        return '({})'.format(', '.join(map(str, self._coordinates)))

    def __len__(self):
        """
        Size of Vector

        :return: int

        """
        return self._size

    def __getitem__(self, item):
        """
        Return vector's coordinate value at `item`

        :param item: int
        :return: number

        """
        return self._coordinates[item]

    def __setitem__(self, key, value):
        """
        Set the `key` coordinate to `value`

        :param key: int
        :param value: number

        :return: number

        """
        self._coordinates[key] = value
        return self._coordinates[key]

    def __add__(self, other):
        """
        Add two vectors and return a result in a new vector

        :param other: Vector
        :raises: ValueError if input vectors have different sizes
        :return: Vector

        """
        if len(self) != len(other):
            raise ValueError('Vectors have different sizes: {} and {}'
                             .format(len(self), len(other)))

        return Vector(a + b for (a, b) in zip(self, other))

    def __iadd__(self, other):
        """
        Add `other` vector to `self` and return resulting summed vector

        :param other: Vector
        :raises: ValueError if input vectors have different sizes
        :return: Vector

        """
        if len(self) != len(other):
            raise ValueError('Vectors have different sizes: {} and {}'
                             .format(len(self), len(other)))

        for i, element in enumerate(other):
            self[i] += element

        return self

    def __neg__(self):
        """
        Change sign of each coordinate in current `self` vector

        :return: Vector

        """
        for i, element in enumerate(self):
            self[i] = -element

        return self

    def __sub__(self, other):
        """
        Substract two vectors and return a result in a new vector

        :param other: Vector
        :raises: ValueError if input vectors have different sizes
        :return: Vector

        """
        if len(self) != len(other):
            raise ValueError('Vectors have different sizes: {} and {}'
                             .format(len(self), len(other)))

        return Vector(a - b for a, b in zip(self, other))

    def __isub__(self, other):
        """
        Substract `other` vector from `self` and return resulting vector

        :param other: Vector
        :raises: ValueError if input vectors have different sizes
        :return: Vector

        """
        if len(self) != len(other):
            raise ValueError('Vectors have different sizes: {} and {}'
                             .format(len(self), len(other)))

        for i, element in enumerate(other):
            self[i] -= element

        return self

    def __eq__(self, other):
        """
        Check if two vectors are equal to each other

        :param other: Vector
        :return: bool
        """
        if len(self) != len(other):
            return False
        return all(self[i] == other[i] for i in range(len(self)))

    def __mul__(self, other):
        """
        If `other` parameter of a number type (int, float, complex) then method
            returns new vector which corresponds to vector constant multiplication

        If `other` parameter is of a Vector type then method returns
            value of a number type which corresponds to scalar product of two vectors.

        :param other: Vector or number (int, float, complex)
        :raises: TypeError if `other` parameter is differs from ones described above
        :raises: ValueError if input vectors have different sizes
        :return: Vector

        """
        if self._is_numeric(other):
            return Vector(other * coordinate for coordinate in self)

        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError('Vectors have different sizes: {} and {}'
                                 .format(len(self), len(other)))

            return sum(a * b for a, b in zip(self, other))


        scalar = self._parse_as(other, Vector.COORDINATE_TYPES)
        return Vector(scalar * coordinate for coordinate in self)

    def __imul__(self, constant):
        """
        Multiply all `self` vector coordinates by `constant`

        :param constant: number
        :return: Vector

        """
        if self._is_numeric(constant):
            for i, element in enumerate(self):
                self[i] *= constant
            return self

        scalar = self._parse_as(constant, Vector.COORDINATE_TYPES)
        for i, element in enumerate(self):
            self[i] *= constant
        return self


class Vector3D(Vector):
    def __init__(self, *args):
        super().__init__(*args)
        if self._size != 3:
            raise TypeError('Vector3D must have exactly 3 coordinates')

    def cross(self, other):
        return Vector3D(
            self[1] * other[2] - other[1] * self[2],
            self[2] * other[0] - other[2] * self[0],
            self[0] * other[1] - other[0] * self[1])


class TestVector3D(unittest.TestCase):
    def test_constructor(self):
        Vector3D(1, 2, 3.0)
        with self.assertRaises(TypeError):
            Vector3D(1)
        with self.assertRaises(TypeError):
            Vector3D(1, 2, 3, 4)

    def test_cross(self):
        v1 = Vector3D(-1, 2, -3)
        v2 = Vector3D(0, -4, 1)
        self.assertEqual(v1.cross(v2), Vector3D(-10, 1, 4))


if __name__ == '__main__':
    unittest.main()
