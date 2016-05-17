from pymongo import MongoClient
import socket

client = MongoClient()
db = client.dns_ip_db
url_ip_coll = db.url_ip_coll
for ip in url_ip_coll.find({'DNS':'Null', 'Attribute': 'PUBLIC'}):
    try:
        print socket.gethostbyaddr(str(ip['IP']))
    except:
        print ip['IP']
