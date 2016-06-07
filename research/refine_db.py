"""refine_db.py.

Refine MongoDB to resolve IPs and DNS names.
"""
import pymongo
import socket
import collections
# from ipwhois import IPWhois
# import datetime

try:
    conn = pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
db = conn.dns_ip_db
url_ip_coll = db.url_ip_coll
dns_dict = collections.Counter()
i = 0
num = url_ip_coll.count()
print num
"""
for ip in url_ip_coll.find({'DNS': 'Null', 'Attribute': 'PUBLIC'}):
    try:
        addr = socket.gethostbyaddr(ip['IP'])
        url_ip_coll.update({'IP': ip['IP']}, {'$set': {'DNS': addr[0]}})
    except:
        url_ip_coll.update({'IP': ip['IP']}, {'$set': {'DNS': 'Unknown'}})
        print 'unknown', i
        i += 1

i = 0

for ip in url_ip_coll.find({'IP': 'Null'}):

    try:
        addr = socket.gethostbyname(ip['DNS'])
        url_ip_coll.update({'DNS': ip['DNS']}, {'$set': {'IP': addr[0]}})
    except:
        url_ip_coll.update({'DNS': ip['DNS']}, {'$set': {'IP': 'Unresolved'}})
        print 'unresolved', i
        i += 1

for ip in url_ip_coll.find({'Attribute': 'PUBLIC'}):
    print ip['IP'], ip['DNS']
"""
