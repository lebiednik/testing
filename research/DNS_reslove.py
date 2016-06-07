import pymongo
import socket
from IPy import IP
from apscheduler.schedulers.blocking import BlockingScheduler

try:
    conn = pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e


def resolve():
    global conn
    # Connection
    dns_ip_db = conn.dns_ip_db
    # Database
    url_ip_coll = dns_ip_db.url_ip_coll
    # Collection
    for ip in url_ip_coll.find({'IP': 'Null'}, no_cursor_timeout=True):
        if url_ip_coll.find({'$and':
                            [{'DNS': ip['DNS']},
                             {"IP": {"$ne": "Null"}}]}).count() > 0:
            res = url_ip_coll.find({'$and':
                                   [{'DNS': ip['DNS']},
                                    {"IP": {"$ne": "Null"}}]})
            url_ip_coll.update({'DNS': ip['DNS']}, {'$set': {'IP': res['IP']}})
        else:
            try:
                addr = socket.gethostbyname(ip['DNS'])
                url_ip_coll.update({'DNS': ip['DNS']}, {'$set': {'IP': addr}})
            except:
                url_ip_coll.update({'DNS': ip['DNS']},
                                   {'$set': {'IP': 'Unresolved'}})

if __name__ == '__main__':
    resolve()
    sched = BlockingScheduler()

    sched.add_job(resolve, 'interval', hours=1)
    sched.start()
"""
{'$and':
[{"date": {"$gt": time2}},
 {"IP": {"$ne": "Null"}},
 {"IP": {"$ne": "Unresolved"}},
 {"Attribute": {"$ne": "PRIVATE"}},
 {"Attribute": {"$ne": "RESERVED"}},
 {"Attribute": {"$ne": "LINK-LOCAL MULTICAST"}},
 {"Attribute": {"$ne": "CARRIER_GRADE_NAT"}}
 ]}
"""
