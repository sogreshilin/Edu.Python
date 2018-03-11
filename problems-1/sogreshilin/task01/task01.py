import unittest

from math import sqrt, ceil


def prime_factor(n):
    last_possible_factor = ceil(sqrt(n))

    factors = []
    factor = 2

    while factor <= last_possible_factor:
        counter = 0
        while n % factor == 0:
            counter += 1
            n //= factor

        if counter > 0:
            factors.append([factor, counter])
        factor += 1

    if n > 1:
        factors.append([n, 1])

    return factors


class TestPrimeFactorization(unittest.TestCase):
    def test_prime(self):
        self.assertEqual(prime_factor(13), [[13, 1]])

    def test_complex(self):
        self.assertEqual(prime_factor(13 * 17), [[13, 1], [17, 1]])
        self.assertEqual(prime_factor(3 ** 4 * 2 ** 6), [[2, 6], [3, 4]])

    def test_zero_one(self):
        self.assertEqual(prime_factor(0), [])
        self.assertEqual(prime_factor(1), [])

    def test_bigint(self):
        factors = [[3, 1], [5, 1], [17, 1], [257, 1], [65537, 1]]
        self.assertEqual(prime_factor(2 ** 32 - 1), factors)

    def test_prime_bigint(self):
        table_prime = 32_416_190_071
        self.assertEqual(prime_factor(table_prime), [[table_prime, 1]])


if __name__ == "__main__":
    unittest.main()
