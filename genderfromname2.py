import requests, codecs
import urllib.request
from requests.utils import quote
from pymongo import MongoClient

testurl = 'http://www.erumy.com/nameAnalyze/AnalyzeMyName.aspx?name='

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
        print("Connected succesfully")
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
            with codecs.open('test2.html', encoding='utf-8', mode='w') as writefile:
                writefile.write(response.read().decode('utf-8'))

        with codecs.open('test2.html', encoding='utf-8', mode='r') as readfile:
            contents = readfile.read()
            with codecs.open('test2.html', encoding='utf-8', mode='w') as writefile:
                writefile.write(contents)

        with codecs.open('test2.html', encoding='utf-8', mode='r') as readfile:
            contents = readfile.read().split('\n')
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
