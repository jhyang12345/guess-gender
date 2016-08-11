import sys, codecs
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from string import ascii_lowercase, ascii_uppercase
from genderfromname import genderfromname

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
    comments = dbh.comments.find({'valid': True, 'gender': ''})
    validcomments = 0
    for comment in comments:
        if not comment['valid']:
            continue
        try:
            print("Evaluating " + comment['name'])
        except:
            dbh.comments.update({'_id': comment['_id']}, {"$set": {"valid": False}})
            continue
        gender = genderfromname(comment['name'])
        print(gender)
        if gender == 'Stopped':
            return
        if gender == 'Unclear':
            dbh.comments.update({'_id': comment['_id']}, {"$set": {"valid": False}})
        else:
            if gender == True or gender == 'male':#male
                dbh.comments.update({'_id': comment['_id']}, {"$set": {"gender": "male"}})
                print(comment['name'] + " is Male" )
            elif gender == False or gender == 'female':
                dbh.comments.update({'_id': comment['_id']}, {"$set": {"gender": "female"}})
                print(comment['name'] + " is Female" )

#        dbh.comments.update({'_id': comment['_id']}, {"$set": {"valid": False}})
#        dbh.comments.update({'_id': comment['_id']}, {"$set": {"message": comment['message'].strip()}})
#        if(checkvalidity(comment.get('name'), comment.get('message'))):
#            validcomments += 1
#            print(comment.get('message'))
#            dbh.comments.update({'_id': comment['_id']}, {"$set": {"valid": True}})

    print(validcomments)


if __name__ == '__main__':
    main()
