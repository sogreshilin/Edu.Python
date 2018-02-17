import math


def is_prime(n):
    last_factor = int(math.sqrt(n))
    return all(n % i for i in range(2, last_factor + 1))


def first_primes_le(n):
    return [i for i in range(2, n) if is_prime(i)]
