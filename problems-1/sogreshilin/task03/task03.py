import math
import bitarray
import time
import unittest


def is_prime(n):
    last_factor = int(math.sqrt(n))
    return all(n % i for i in range(2, last_factor + 1))


def eratosthenes_list(upper_bound):
    sieve = list(range(upper_bound))

    for i in range(2, int(math.sqrt(upper_bound)) + 1):
        for j in range(i * 2, upper_bound, i):
            sieve[j] = 0

    return [value for (index, value) in enumerate(sieve) if index > 1 and value != 0]


def eratosthenes_set(upper_bound):
    sieve = set(range(2, upper_bound))

    for i in range(2, int(math.sqrt(upper_bound)) + 1):
        for j in range(i * 2, upper_bound, i):
            if j in sieve: sieve.remove(j)

    return sieve


def eratosthenes_bitarray(upper_bound):
    bits = bitarray.bitarray(upper_bound)
    bits.setall(True)

    for i in range(2, int(math.sqrt(upper_bound)) + 1):
        for j in range(i * 2, upper_bound, i):
            bits[j] = False

    return [i for i in range(2, upper_bound) if bits[i]]


def measure_time(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    return time.time() - start_time


class TestEratosthenes(unittest.TestCase):
    small_n = 10_000
    big_n = 100_000_000

    def test_simple(self):
        self.assertEqual(eratosthenes_list(3), [2])

    def test_list(self):
        pass
        self.assertTrue(all(is_prime(n) for n in eratosthenes_list(self.small_n)))

    def test_set(self):
        self.assertTrue(all(is_prime(n) for n in eratosthenes_set(self.small_n)))

    def test_bitarray(self):
        self.assertTrue(all(is_prime(n) for n in eratosthenes_bitarray(self.small_n)))

    def test_raises_type_error(self):
        with self.assertRaises(TypeError):
            eratosthenes_list("string_value")

    def test_time(self):
        list_time = measure_time(eratosthenes_list, self.big_n)
        set_time = measure_time(eratosthenes_set, self.big_n)
        bitarray_time = measure_time(eratosthenes_bitarray, self.big_n)
        print()
        print("Time test results:")
        print(" - list : {0:.4f}".format(list_time))
        print(" - set  : {0:.4f}".format(set_time))
        print(" - bits : {0:.4f}".format(bitarray_time))


def main():
    unittest.main()


if __name__ == "__main__":
    main()
