import requests, codecs, html
import urllib.request
from requests.utils import quote
from pymongo import MongoClient

testurl = 'http://www.erumy.com/nameAnalyze/AnalyzeMyName.aspx?name='
anotherurl = 'https://www.facebook.com/app_scoped_user_id/482117105305550/'

def grablength(line):
    ret = ''
    pxind = line.index('px')
    while(True):
        pxind -= 1
        if line[pxind] == '"':
            break
        ret = line[pxind] + ret
    return int(ret)


def genderfromname(name, tries=3):
#    name = '김옥선'
    testurl = 'http://www.erumy.com/nameAnalyze/AnalyzeMyName.aspx?name='

    testurl = testurl + quote(name)

    try:
        c = MongoClient(host='localhost', port=27017)
        print("Connected successfully")
    except ConnectionFailure as e:
        sys.stderr.write("Connection failed.")
        sys.exit(1)
    dbh = c['commentdb']
    try:
        checkfirst = dbh.namegender.find_one({'name': name})
    except UnicodeError as e:
        sys.stderr.write("Failed to read characters.")
        return "Stopped"

    if checkfirst:
        return checkfirst['gender']
    men = 0
    women = 0
    try:
        with urllib.request.urlopen(testurl) as response:
            contents = codecs.decode(response.read(), 'utf-8')
            contents = contents.split('\n')
            print(contents)
            for line in contents:
                if '남자' in line and '<img src' in line:
                    men = grablength(line)
                if '여자' in line and '<img src' in line:
                    women = grablength(line)
        print(men, women)

        if men > women * 2:
            dbh.namegender.insert({'name': name, 'gender': 'male'})
            return True#return true for man
        elif men * 2 < women:
            dbh.namegender.insert({'name': name, 'gender': 'female'})
            return False#return false for women
        dbh.namegender.insert({'name': name, 'gender': 'unclear'})
        return "Unclear"
    except:
        if tries > 0:
            return genderfromname(name, tries - 1)
        else:
            return "Stopped"

if __name__ == '__main__':
    print(genderfromname('김옥선'))
