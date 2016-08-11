import sys, codecs
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from string import ascii_lowercase, ascii_uppercase
from genderfromname2 import genderfromname

def checkvalidity(name, message):
    for x in name:
        if x in ascii_lowercase or x in ascii_uppercase:
            return False
    for x in message:
        if x in ascii_lowercase or x in ascii_uppercase:
            return False
    if len(message) < 20:
        return False
    if message.count('\n') >= 5:
        return False
    return True


def main():
    try:
        c = MongoClient(host="localhost", port=27017)
    except ConnectionFailure as e:
        sys.stderr.write("Connection failed.")
        sys.exit(1)
    dbh = c['commentdb']
    comments = dbh.nextcomments.find({'valid': True, 'gender': {'$ne': ''}})#.count()
    totalcomments = comments.count()
    print(comments)
    validcomments = 0
    evaluated = 0
    commentsinserted = 0

    print("Total Comments: " + str(totalcomments) + " Comments Inserted: " + str(commentsinserted))


if __name__ == '__main__':
    main()
