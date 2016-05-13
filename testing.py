import sys
import os
import collections

def running():
    list1 = ('b', 'a', 'b', 'a', 'b', 'c', 'd', 'e', 'e', 'a', 'g')
    dict1 = collections.Counter()
    topdict = {}
    for word in list1:
        dict1[word] += 1
    for k, v in dict1.most_common(3):
        print '%s: %i' % (k,v)

            
    print topdict

if __name__ == '__main__':
    running()

