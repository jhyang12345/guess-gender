from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def main():
    try:
        c = MongoClient(host='localhost', port=27017)
        print("Connected successfully.")
    except ConnectionFailure as e:
        sys.stderr.write("Connection failed.")
        sys.exit(1)
    dbh = c['commentdb']
    malecounts = dbh.comments.find({'gender': 'male'}).count()
    femalecounts = dbh.comments.find({'gender': 'female'}).count()
    print(malecounts, femalecounts)

if __name__ == '__main__':
    main()
