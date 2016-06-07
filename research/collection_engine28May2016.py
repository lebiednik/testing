"""
Collection engine for research project.

Author: Brian Lebiednik
"""
import collections
import requests
import datetime
import pymongo
import socket
from IPy import IP
from apscheduler.schedulers.blocking import BlockingScheduler

try:
    conn = pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e

ENDPOINTS = {
    'dns_queries': {
        '/stats/dns_queries': {'view': 'raw', 'alexa': True},
    },
    'ip_access': {
        '/stats/ip_access': {'port': '443', 'port': '80'},
    }  # ,
    # 'av': {
    #    '/stats/av/detection_summary': {'view': 'hash'},
    # }TODO: use the number of samples to collect more information

}
BASE_URL = 'https://apiary.gtri.gatech.edu'


def collect_samples():
    """Connect to the Apiary API and collect samples."""
    hours = 1
    key = '/home/brian/Documents/testing/research/Brian_unencrypted_key.pem'
    global conn
    # connection

    # conn.drop_database("dns_ip_db")
    # clears the db for testing
    dns_ip_db = conn.dns_ip_db
    # Database
    url_ip_coll = dns_ip_db.url_ip_coll
    # Collection

    session = requests.session()

    dns_dict = collections.Counter()
    ip_dict = collections.Counter()

    for name in ENDPOINTS:
        for endpoint, parameters in ENDPOINTS[name].iteritems():
            url = '{}/api/v1{}'.format(BASE_URL, endpoint)
            parameters['hours'] = hours

            try:
                resp = session.get(url, params=parameters, cert=key)
                resp.raise_for_status()
            except requests.HTTPError:
                print 'HTTP body: {}, \nurl: {}'.format(
                    resp.text, url)
                continue

            else:
                data = resp.json()

                for doc in data.get('results', []):
                    if name == 'dns_queries':
                        if doc['alexa'] == -1:
                            doc['alexa'] = 1000001
                        dns_dict[doc["domain"]] += len(doc["hashes"])
                        url_ip_coll.insert_one({'Initial Type': 'DNS',
                                                'IP': 'Null',
                                                'DNS': doc["domain"],
                                                'seen': len(doc["hashes"]),
                                                'Attribute': 'Unknown',
                                                'Alexa': doc['alexa'],
                                                'date':
                                                datetime.datetime.now(),
                                                'Hidden': 'False'})

                    elif name == 'ip_access':
                        ip_dict[doc["ip"]] += len(doc["hashes"])
                        ip2 = IP(doc["ip"])
                        url_ip_coll.insert_one({'Initial Type': 'IP',
                                                'IP': doc["ip"],
                                                'DNS': 'Null',
                                                'seen': len(doc["hashes"]),
                                                'Attribute': ip2.iptype(),
                                                'Alexa': 'Unknown',
                                                'date':
                                                datetime.datetime.now(),
                                                'Hidden': 'False'})


def process_db():
    """collect some of the data and display it."""
    global conn
    # Connection
    dns_ip_db = conn.dns_ip_db
    # Database
    url_ip_coll = dns_ip_db.url_ip_coll
    # Collection
    dns_dict = collections.Counter()
    ip_dict = collections.Counter()
    alexa = 10000
    top_number = 20
    for ip in url_ip_coll.find({'IP': 'Null'}):

        try:
            addr = socket.gethostbyname(ip['DNS'])
            url_ip_coll.update({'DNS': ip['DNS']}, {'$set': {'IP': addr}})
        except:
            url_ip_coll.update({'DNS': ip['DNS']},
                               {'$set': {'IP': 'Unresolved'}})

    for ip in url_ip_coll.find({'Attribute': 'PUBLIC'}):
        ip_dict[ip['IP']] += ip['seen']

    for dns in url_ip_coll.find({'Alexa': {"$gt": alexa}}):
        dns_dict[dns['DNS']] += dns['seen']
    print '\n Top {} DNS request:'.format(top_number)
    for k, v in dns_dict.most_common(top_number):
        print '%s: %i' % (k, v)
    print '\n Top {} IP request:'.format(top_number)
    for k, v in ip_dict.most_common(top_number):
        print '%s: %i' % (k, v)


def clean_db():
    """Remove old data."""
    global conn
    # Connection
    dns_ip_db = conn.dns_ip_db
    # Database
    url_ip_coll = dns_ip_db.url_ip_coll
    # Collection
    time2 = datetime.datetime.now() - datetime.timedelta(days=14)
    url_ip_coll.remove({"date": {"$lt": time2}})
    print 'Last run {}'.format(datetime.datetime.now())


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
    collect_samples()
    process_db()
    clean_db()
    set_benign()
    sched = BlockingScheduler()

    sched.add_job(collect_samples, 'interval', hours=1)
    sched.add_job(process_db, 'interval', hours=1)
    sched.add_job(clean_db, 'interval', hours=1)
    sched.add_job(set_benign, 'interval', hours=1)
    sched.start()
