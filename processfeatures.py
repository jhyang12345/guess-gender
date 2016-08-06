from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from collections import defaultdict

def main():
    try:
        c = MongoClient(host='localhost', port=27017)
        print("Connected successfully")
    except:
        sys.stderr.write("Connection failed.")
        sys.exit(1)
    dbh = c['commentdb']
    women = dbh.commentfeatures.find({'gender': 'female'})
    men = dbh.commentfeatures.find({'gender': 'male'})
    menmean = defaultdict(float)
    womenmean = defaultdict(float)

    for comment in men:
    #    print(comment.keys())
        menmean['spacings'] += comment['spacings']
        menmean['nonvowel'] += comment['nonvowel']
        menmean['punctuation'] += comment['punctuation']
    for comment in women:
    #    print(comment.keys())
        womenmean['spacings'] += comment['spacings']
        womenmean['nonvowel'] += comment['nonvowel']
        womenmean['punctuation'] += comment['punctuation']
    for key in menmean.keys():
        print(key)
        print(menmean[key] / men.count())
        print(womenmean[key] / women.count())

    print("Number of Men: " + str(men.count()))
    print("Number of Women: " + str(women.count()))


if __name__ == '__main__':
    main()
