import unittest


class Vector:
    """
    Vector class represents one-dimensional mathematical vector.
    Vector has typical for vector operations.

    """

    def __init__(self, coordinates):
        """
        Create vector with specified coordinates.
        The size of vector cannot be changed after vector construction.

        :param coordinates: list or tuple of int, float or double elements
        
        """
        if any(not isinstance(c, (int, float, complex)) for c in coordinates):
            raise ValueError('Invalid coordinate type: must be a number')
        self._size = len(coordinates)
        self._coordinates = coordinates

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

        coordinates = list()
        for i in range(len(self)):
            coordinates.append(self[i] + other[i])

        return Vector(coordinates)

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

        for i in range(len(self)):
            self[i] += other[i]

        return self

    def __neg__(self):
        """
        Change sign of each coordinate in current `self` vector

        :return: Vector

        """
        for i in range(len(self)):
            self[i] = -self[i]

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

        coordinates = list()
        for i in range(len(self)):
            coordinates.append(self[i] - other[i])

        return Vector(coordinates)

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

        for i in range(len(self)):
            self[i] -= other[i]

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
        if isinstance(other, (int, float, complex)):
            coefficients = list()
            for i in range(len(self)):
                coefficients.append(self[i] * other)
            return Vector(coefficients)

        elif not isinstance(other, Vector):
            raise TypeError('Unexpected argument type found: {}'.format(type(other)))

        if len(self) != len(other):
            raise ValueError('Vectors have different sizes: {} and {}'
                             .format(len(self), len(other)))

        scalar_product = 0
        for i in range(len(self)):
            scalar_product += self[i] * other[i]

        return scalar_product

    def __imul__(self, constant):
        """
        Multiply all `self` vector coordinates by `constant`

        :param constant: number
        :return: Vector

        """
        if isinstance(constant, (int, float, complex)):
            for i in range(len(self)):
                self[i] *= constant
            return self

        raise TypeError('Unexpected argument type found: {}'.format(type(constant)))


class TestVector(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            Vector(['a', 'b', 'c'])

    def test_add(self):
        v1 = Vector.ones(3)
        v2 = Vector([-1, -1, -1])
        self.assertEqual(v1 + v2, Vector.zeros(3))

        v3 = Vector([])
        v4 = Vector([])
        self.assertEqual(v3 + v4, v3)

        with self.assertRaises(ValueError):
            v1 = v1 + v3

    def test_iadd(self):
        v1 = Vector([0, 1, 2])
        v1 += Vector([1, 0, -1])
        self.assertEqual(v1, Vector.ones(3))

    def test_sub(self):
        v1 = Vector([-1, 0, 1])
        self.assertEqual(v1 - v1, Vector.zeros(3))
        self.assertEqual(v1 - v1 - v1, -v1)

        with self.assertRaises(ValueError):
            v1 = v1 + Vector.ones(4)

    def test_isub(self):
        v1 = Vector([0, 1, 2])
        v1 -= Vector([1, 0, -1])
        self.assertEqual(v1, Vector([-1, 1, 3]))
        with self.assertRaises(ValueError):
            v1 -= Vector([])

    def test_mul_scalar(self):
        v1 = Vector([1, 2, 3])
        self.assertEqual(v1 * 2, Vector([2, 4, 6]))
        self.assertEqual(v1 * 2.5, Vector([2.5, 5.0, 7.5]))
        self.assertEqual(v1 * complex(1.0, 1.0), \
                         Vector([
                             complex(1.0, 1.0),
                             complex(2.0, 2.0),
                             complex(3.0, 3.0),
                         ]))
        with self.assertRaises(TypeError):
            v1 = v1 * '42'

    def test_imul(self):
        v1 = Vector([1, 2, 3, 4])
        v1 *= 2
        self.assertEqual(v1, Vector([2, 4, 6, 8]))
        v1 *= 0.5
        self.assertEqual(v1, Vector([1, 2, 3, 4]))

    def test_mul_vector(self):
        v1 = Vector.ones(3)
        v2 = Vector([1, 2, 3])
        self.assertEqual(v1 * v2, 6)
        self.assertEqual(v1 * Vector.zeros(3), 0)
        self.assertEqual(v1 * (-v2), -6)
        with self.assertRaises(ValueError):
            v1 = v1 * Vector([])

    def test_imul_vector(self):
        with self.assertRaises(TypeError):
            v1 = Vector([])
            v1 *= Vector([])

    def test_equals(self):
        v1 = Vector([0, 0])
        v2 = Vector([1, 0])
        self.assertNotEqual(v1, v2)
        self.assertEqual(v1, v2 * 0)
        self.assertNotEqual(v1, Vector.zeros(3))

    def test_len(self):
        v1 = Vector(list(range(10)))
        self.assertEqual(len(v1), 10)
        v2 = Vector(list(range(100)))
        self.assertEqual(len(v2), 100)
        v3 = Vector([])
        self.assertEqual(len(v3), 0)

    def test_getitem(self):
        v1 = Vector(list(range(10)))
        self.assertTrue(all(i == v1[i] for i in range(10)))
        with self.assertRaises(IndexError):
            element = v1[100]

    def test_setitem(self):
        v1 = Vector(list(range(10)))
        for i in range(len(v1)):
            v1[i] = 0
        self.assertEqual(v1, Vector.zeros(10))

    def test_str(self):
        v1 = Vector.zeros(3)
        self.assertEqual(v1.__str__(), '(0, 0, 0)')
        v2 = Vector.ones(2)
        self.assertEqual(v2.__str__(), '(1, 1)')


if __name__ == '__main__':
    unittest.main()


