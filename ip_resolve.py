import pymongo
import socket
import collections
from ipwhois import IPWhois
from pprint import pprint

try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e

db = conn.dns_ip_db
url_ip_coll = db.url_ip_coll
dns_dict = collections.Counter()
for ip in url_ip_coll.find({'DNS':'Null', 'Attribute': 'PUBLIC'}):
    dns_dict[ip['IP']] += ip['seen']
for k, v in dns_dict.most_common(10):
    print '%s: %i' %(k,v)
    """try:
        print socket.gethostbyaddr(str(k))
    except:
        print ip['IP']
    """#try:
    obj = IPWhois(str(k))
    results = obj.lookup_rdap(depth=1)
    print results['asn_country_code'], results['asn_registry']
    #except:
    #    print "IPWhois Failed"
