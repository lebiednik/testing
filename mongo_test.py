import pymongo

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e

"""
posts.update({"_id":1234},{"$inc":{"total_posts":9}})
posts.find_one({"_id":1234})
"""
