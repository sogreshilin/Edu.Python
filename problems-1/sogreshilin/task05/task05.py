import math
import unittest


def is_prime(n):
    if n < 2:
        return False
    last_factor = int(math.sqrt(n))
    return all(n % i for i in range(2, last_factor + 1))


def first_primes_le(n):
    return [i for i in range(2, n + 1) if is_prime(i)]


class TestPrimes(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(first_primes_le(0), [])

    def test_one(self):
        self.assertEqual(first_primes_le(1), [])

    def test_le_prime(self):
        self.assertEqual(first_primes_le(3), [2, 3])

    def test_le_non_prime(self):
        self.assertEqual(first_primes_le(9), [2, 3, 5, 7])


if __name__ == "__main__":
    unittest.main()
