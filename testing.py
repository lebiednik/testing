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
    url2 = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    url3 = '((ftp|http|https):\/\/)?([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+.*)'
    url4 = '((ftp|http|https):\/\/)?([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+.*)'
    url5 = 'http[s]?://(?:[a-zA-Z0-9]|[0-9]|[$-_@.&+]|[!*\(\),\~]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    """
    File has 925 true URLs and 4 BS entries
    url:912
    doesnt get the BS data but doesnt get www2
    url2: 925
    misses ~ but doesnt get the BS
    url3:927
    gets the BS data
    url4: no change to url3 same working copy
    url5: 925
    fixed
    """
    f = open('url_list.txt')
    dict2 = collections.Counter()
    for line in f:
        m = re.findall(url5, line)
        for i in m:
            try:
                dict2[i] +=1
                count += 1
                if count > 908:
                    print i
            except:
                pass

        #print m
    print count
    for k, v in dict2.most_common(3):
        print '%s: %i' % (k,v)
    print dict2['http://no.shvoong.com/exact-sciences/chemistry/chemical-physics/']
    print dict2['http://www2.math.uic.edu/~jan/Demo/quadgrid.html']

if __name__ == '__main__':
    running()
