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
    men = dbh.commentfeatures.find({'gender': 'male'})
    women = dbh.commentfeatures.find({'gender': 'female'})
    menlist = []
    for feature in men:
        menlist.append(feature)
    womenlist = []
    for feature in women:
        womenlist.append(feature)
    mensample = random.sample(menlist, 4000)
    womensample = random.sample(womenlist, 4000)
    menvalid = []
    womenvalid = []
    for feature in menlist:
        if feature not in mensample:
            menvalid.append(feature)
    for feature in womenlist:
        if feature not in womensample:
            womenvalid.append(feature)
    print(len(menvalid), len(womenvalid))
    dbh.trainingsample.remove({})
    dbh.validationsample.remove({})
    for sample in mensample + womensample:
        sample.pop('_id')
        dbh.trainingsample.insert_one(sample)
    for sample in menvalid + womenvalid:
        sample.pop('_id')
        dbh.validationsample.insert_one(sample)
    print(dbh.validationsample.find({}).count())
    print(dbh.trainingsample.find({}).count())


if __name__ == '__main__':
    main()
