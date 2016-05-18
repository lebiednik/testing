import sys
import os
from sys import argv
import re
fib = []
primes = [2]

def fibonacci(limit):
    x = 1
    y = 2
    global fib
    fib.append(x)
    fib.append(y)
    while (y+x < limit +1):
        z = x +y
        x = y
        y = z
	#print fib
        fib.append(z)

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
    for x in xrange(2, limit):
        if is_prime(x):
             primes.append(x)

    
        

if __name__ == '__main__':
    """
    n = 600851475143
    i = 2
    while i *i <n:
        while n%i ==0:
            n = n/i
        i = i +1
    print n 
    for x in range(900, 1000):
        for y in range(900, 1000):
            z = x*y
            if str(z) == str(z)[::-1]:
                print z 
    """
    num = 2
    test = 10
    for x in range(1, test+1):
        while (num%x !=0):
            num = num +2
    print num
        
