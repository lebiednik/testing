import pymongo
import socket
import collections
from ipwhois import IPWhois
from pprint import pprint
import datetime

try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e

db = conn.dns_ip_db
url_ip_coll = db.url_ip_coll
dns_dict = collections.Counter()
time2 = datetime.datetime.now() -datetime.timedelta(days=7)
for ip in url_ip_coll.find({'DNS':'Null', 'Attribute': 'PUBLIC', "date": {"$gt": time2}}):
    dns_dict[ip['IP']] += ip['seen']
    #obj = IPWhois(str(ip['IP']))
    #results = obj.lookup_rdap(depth=1)

    #sec_result = results['network']
    #print sec_result['name']
    #try
for k, v in dns_dict.most_common(20):
    print '%s: %i' %(k,v)

    obj = IPWhois(str(k))
    results = obj.lookup_rdap(depth=1)
    sec_result = results['network']
    print results['asn_country_code'], results['asn_registry'], sec_result['name']
    try:
        addr = socket.gethostbyaddr(str(k))
        print addr, addr[0]
    except:
        print 'Unknown host'


    #except:
    #    print "IPWhois Failed"
