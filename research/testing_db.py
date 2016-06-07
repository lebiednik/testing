"""testing_db.py.

Checking to make sure everything is working.
"""
import pymongo
import collections
import datetime


try:
    conn = pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e

db = conn.dns_ip_db
url_ip_coll = db.url_ip_coll
ip_list = []
dns_list = []
for x in range(24, 1, -2):
    ip_dict = collections.Counter()
    dns_dict = collections.Counter()
    print 'Time ago %i' % x
    time2 = datetime.datetime.now() - datetime.timedelta(hours=x)
    for ip in url_ip_coll.find({'$and':
                                [{"date": {"$gt": time2}},
                                 {"IP": {"$ne": "Null"}},
                                 {"IP": {"$ne": "Unresolved"}},
                                 {"Attribute": {"$ne": "PRIVATE"}},
                                 {"Attribute": {"$ne": "RESERVED"}},
                                 {"Attribute": {"$ne": "LINK-LOCAL MULTICAST"}},
                                 {"Attribute": {"$ne": "CARRIER_GRADE_NAT"}}
                                 ]}):
        if ip['IP'] in ip_list:
            ip_list.append(ip['IP'])
        else:
            ip_dict[ip['IP']] += ip['seen']
    for k, v in ip_dict.most_common(20):
        print '%s: %i' % (k, v)
    for dns in url_ip_coll.find({'$and':
                                 [{'date': {'$gt': time2}},
                                  {'DNS': {'$ne': 'Null'}},
                                  {'Hidden': 'False'}
                                 ]}):
        if dns['DNS'] in dns_list:
        dns_dict[dns['DNS']] += dns['seen']
    for k, v in dns_dict.most_common(20):
        print '%s: %i' % (k, v)
