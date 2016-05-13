import sys
import os
import collections
import re

def running():
    list1 = ('b', 'a', 'b', 'a', 'b', 'c', 'd', 'e', 'e', 'a', 'g')

    list2 = []
    """
    with open('testfile.txt') as f:
        list2 = [x.strip('\n') for x in f.readlines()]

    print list2
    dict1 = collections.Counter()
    for word in list2:
        dict1[word] += 1
    for k, v in dict1.most_common(3):
        print '%s: %i' % (k,v)

    """
    list3 = []
    count = 0
    url = '(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    f = open('url_list.txt')
    dict2 = collections.Counter()
    for line in f:
        m = re.findall(url, line)
        for i in m:
            try:
                dict2[i] +=1
            except:
                pass
        count += 1
        #print m
    print count
    for k, v in dict2.most_common(3):
        print '%s: %i' % (k,v)


if __name__ == '__main__':
    running()
