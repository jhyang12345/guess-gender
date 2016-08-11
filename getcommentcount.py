from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    c = MongoClient(host='localhost', port=27017)
except ConnectionFailure as e:
    sys.stderr.write("Connection failed.")
    sys.exit(1)

dbh = c['commentdb']

comments = dbh.comments.find({}).count()
print(comments)
