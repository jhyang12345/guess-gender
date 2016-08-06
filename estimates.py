from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import math, copy, random

def main():
    try:
        c = MongoClient(host='localhost', port=27017)
    except ConnectionFailure as e:
        sys.stderr.write("Connection failed.")
        sys.exit(1)
    dbh = c['commentdb']
    
