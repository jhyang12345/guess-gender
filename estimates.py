from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import math, copy, random
from logistictraining import h

def main():
    try:
        c = MongoClient(host='localhost', port=27017)
    except ConnectionFailure as e:
        sys.stderr.write("Connection failed.")
        sys.exit(1)
    dbh = c['commentdb']
    total = dbh.validationsample.find({})
    theta = dbh.theta.find({})[0]

    count = 0
    for feature in total:
        answer = feature.pop('gender')
        prediction = ''
        if h(feature, theta) > 0.5:
            prediction = 'male'
        else:
            prediction = 'female'
        print(answer, prediction)
        if prediction == answer:
            count += 1
    print(count)
    print(count / total.count() * 100)


if __name__ == '__main__':
    main()
