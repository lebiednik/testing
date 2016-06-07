"""working_db.py.

Looking through searches for interesting information.
"""
import pymongo
import socket
import collections
# from ipwhois import IPWhois
# from pprint import pprint
import datetime
import re
import enchant

try:
    conn = pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e

db = conn.dns_ip_db
url_ip_coll = db.url_ip_coll
ip_dict = collections.Counter()
dns_dict = collections.Counter()
top_number = 40
num = url_ip_coll.count()
d = enchant.Dict("en_US")
"""
print num
time2 = datetime.datetime.now() - datetime.timedelta(days=7)
for ip in url_ip_coll.find({'$and':
                            [{"date": {"$gt": time2}},
                             {"IP": {"$ne": "Null"}},
                             {"IP": {"$ne": "Unresolved"}},
                             {"Attribute": {"$ne": "PRIVATE"}},
                             {"Attribute": {"$ne": "RESERVED"}},
                             {"Attribute": {"$ne": "LINK-LOCAL MULTICAST"}},
                             {"Attribute": {"$ne": "CARRIER_GRADE_NAT"}}
                             ]}):
    ip_dict[ip['IP']] += ip['seen']
    # "date": {"$gt": time2}})
for k, v in ip_dict.most_common(1):
    print '%s: %i' % (k, v)

for ip in url_ip_coll.find({'$and':
                            [{"date": {"$gt": time2}},
                             {"DNS": {"$ne": "Null"}},
                             {"DNS": {"$ne": "Unknown"}},
                             {'Hidden': 'False'}
                             ]}):
    dns_dict[ip['DNS']] += ip['seen']
    # "date": {"$gt": time2}})
f = open('top_dns.txt', 'w')
for k, v in dns_dict.most_common()[:-30-1:-1]:
    # f.write(k)
    # f.write('\n')
    print '%s: %i' % (k, v)
    match = re.split('\.', str(k))
    if not d.check(match[0]):
        print match[0]
for k, v in dns_dict.most_common(30):
    # f.write(k)
    # f.write('\n')
    print '%s: %i' % (k, v)
    match = re.split('\.', str(k))
    if not d.check(match[0]) or d.check(match[1]):
        print match[0]

regex = re.compile('google', re.IGNORECASE)
print 'starting regex search'
f.write('Google \n')
for ip in url_ip_coll.find({'$and':
                            [{'DNS': regex},
                             {'Hidden': {'$ne': 'True'}}]}):
    f.write(ip['DNS'])
    f.write('\n')
f.write('\n Microsoft \n')
regex = re.compile('microsoft', re.IGNORECASE)
for ip in url_ip_coll.find({'$and':
                            [{'DNS': regex},
                             {'Hidden': {'$ne': 'True'}}]}):
    f.write(ip['DNS'])
    f.write('\n')
f.write('windows \n')
regex = re.compile('windows', re.IGNORECASE)
for ip in url_ip_coll.find({'$and':
                            [{'DNS': regex},
                             {'Hidden': {'$ne': 'True'}}]}):
    f.write(ip['DNS'])
    f.write('\n')

"""
i = 0
for ip in url_ip_coll.find({'IP': 'Unresolved'}):
    i += 1
print i
"""
    try:
        addr = socket.gethostbyname(ip['DNS'])
        url_ip_coll.update({'DNS': ip['DNS']}, {'$set': {'IP': addr}})
    except:
        pass
"""
