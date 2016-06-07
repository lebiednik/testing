import pymongo

try:
    conn = pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e

def set_benign():
    """Set well known sites to Hidden."""
    global conn
    # Connection
    dns_ip_db = conn.dns_ip_db
    # Database
    url_ip_coll = dns_ip_db.url_ip_coll
    # Collection

    url_ip_coll.update({'DNS': 'www.google.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'google.com'}, {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'www.download.windowsupdate.com'},
                       {'$set': {'Hidden': 'True'}}, multi=True)
    url_ip_coll.update({'DNS': 'download.windowsupdate.com'},
                       {'$set': {'Hidden': 'True'}}, multi=True)
    url_ip_coll.update({'DNS': 'twitter.com'}, {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'pki.google.com'}, {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'apis.google.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'maps.google.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'www.virustotal.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'microsoft.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'dns.msftncsi.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'clients1.google.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'ocsp.godaddy.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'www.microsoft.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'ocsp.verisign.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'ocsp.digicert.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)
    url_ip_coll.update({'DNS': 'go.microsoft.com'},
                       {'$set': {'Hidden': 'True'}},
                       multi=True)

if __name__ == '__main__':
    set_benign()
