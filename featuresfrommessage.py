import jamo
from jamo import h2j, j2hcj
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from collections import Counter, defaultdict
from string import punctuation
import codecs
import string as punc

def getnonvowel(string):#초성 사용 빈도
    total = 0
    jamos = 0
    for letter in string:
        if jamo.is_hangul_char(letter):
            total += 1
        elif jamo.is_jamo(letter):
            jamos += 1
            total += 1

    return jamos / total if total != 0 else 0

def spacings(string):
    total = len(string)
    spaces = 0
    for x in string:
        if x == ' ':
            spaces += 1
    return spaces / total

def punctuationcount(message):
    total = len(message)
    count = 0
    for x in message:
        if x in punc.punctuation:
            count += 1
    return count / total

def dividehangul(string):
    realletter = 0
    realtail = 0
    headcounts = defaultdict(int)
    vowelcounts = defaultdict(int)
    tailcounts = defaultdict(int)
    headfound = set()
    vowelfound = set()
    tailfound = set()

    for letter in string:
        parts = jamo.j2hcj(jamo.h2j(letter))
        if len(parts) > 2:
            head = parts[0]
            vowel = parts[1]
            tail = parts[2]
            realletter += 1#realletter equals realvowel
            realtail += 1#find list of jamo
            headfound.add(head)
            vowelfound.add(vowel)
            tailfound.add(tail)
            headcounts[head] += 1
            vowelcounts[vowel] += 1
            tailcounts[tail] += 1

        elif len(parts) > 1:
            head = parts[0]
            vowel = parts[1]
            realletter += 1
            headfound.add(head)
            vowelfound.add(vowel)
            headcounts[head] += 1
            vowelcounts[vowel] += 1

    headp = {}
    vowelp = {}
    tailp = {}

    with codecs.open('headjamo.txt', encoding='utf-8', mode='r') as f:
        for x in f.read().strip():
            headp[x] = headcounts[x] / realletter if realletter != 0 else 0
    with codecs.open('voweljamo.txt', encoding='utf-8', mode='r') as f:
        for x in f.read().strip():
            vowelp[x] = vowelcounts[x] / realletter if realletter != 0 else 0
    with codecs.open('tailjamo.txt', encoding='utf-8', mode='r') as f:
        for x in f.read().strip():
            tailp[x] = tailcounts[x] / realtail if realtail != 0 else 0
    return (headp, vowelp, tailp)

def main():
    try:
        c = MongoClient(host='localhost', port=27017)
        print("Connected successfully")
    except ConnectionFailure as e:
        sys.stderr.write("Connection failed.")
        sys.exit(1)
    dbh = c['commentdb']
    comments = dbh.comments.find({'valid': True, 'gender': {'$ne': ''}})
    number = 0
    print(dbh.commentfeatures.find({}).count())
    #result = dbh.commentfeatures.delete_many({})
    #print(result.deleted_count)
"""    for comment in comments:
        features = {}
        features['gender'] = comment['gender']
        message = comment['message'].strip()
        features['nonvowel'] = getnonvowel(message)
        features['spacings'] = spacings(message)
        features['head'], features['vowel'], features['tail'] = dividehangul(message)
        features['punctuation'] = punctuationcount(message)
        print("Inserting " + comment['name'],message, number)
        number += 1
        dbh.commentfeatures.insert(features)
"""


if __name__ == '__main__':
    main()
