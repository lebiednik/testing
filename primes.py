import sys
import os

primes = []

def is_prime(num):
    global primes
    for x in primes:
        if (num/2 < x):
            return True 
        elif (num%x == 0):
            return False
    return True


def total_primes(limit):
    global primes
    for x in range(2, limit):
        if is_prime(x):
             primes.append(x)


if __name__ == '__main__':
    total_primes(30)
    print primes
