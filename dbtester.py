from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def main():
    try:
        c = MongoClient(host='localhost', port=27017)
        print(c.test)
        #c = MongoClient(host="localhost", port=27017)
        print("Connected successfully")
    except ConnectionFailure as e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)

    dbh = c["mydb"]

    user_doc = {
        "username" : "janedoe",
        "firstname": "Jane",
        "surname": "Doe",
        "dateofbirth": datetime(1974, 4, 12),
        "email": "janedoe74@example.com",
        "score" : 0
    }

    dbh.users.insert(user_doc)

    print("Successfully set up a handle")



if __name__ == '__main__':
    main()
