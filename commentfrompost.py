import facebook, requests, sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from getgender import checkvalidity

totalcomments = 0

mytoken = ''
with open('mytoken.txt', 'r') as token:
    mytoken = token.read().strip()

graph = facebook.GraphAPI(access_token=mytoken, version='2.0')

count = 0
def getname(user):#need to query user again
    try:
        user = graph.get_object(id=user['id'], connection_name="user")
        return user['name']
    except:
        return ''
    return ''


def commentfrompost(postid):
    checkurl = ''
    post = None
    try:
        post = graph.get_object(id=postid, connection_name="post")
    except:
        return []
    comments = None
    ret = []
    print("Trying postid: " + postid)
    try:
        comments = post['comments']
        print("Comments found!")
    except:
        return []
    for x in range(30):
        newurl = ''
        try:
            newurl = comments['paging']['next']
        except:
            newurl = "None here"
            break

        for comment in comments['data']:
            try:
                if comment['message'] != None and checkvalidity("", comment['message']):
                    if(len(comment['message']) >= 15):
                        print(comment['message'])
                        addcomment = {}
                        addcomment['name'] = getname(comment['from'])
                        addcomment['message'] = comment['message'].strip()
                        addcomment['gender'] = ''
                        addcomment['valid'] = True
                        ret.append(addcomment)
                        totalcomments += 1
            except:
                continue

            #print(comment.keys())
    #    print(comments['paging'])
        comments = requests.get(comments['paging']['next']).json()
    #    post = requests.get(post['paging']['next']).json()
    return ret

def main():
    commentssaved = 0
    with open('newpostids.in', 'r') as postid:
        try:
            c = MongoClient(host='localhost', port=27017)
            print("Connected succesfully")
        except ConnectionFailure as e:
            sys.stderr.write("Connection failed.")
            sys.exit(1)
        totalidsread = []
        with open('newpostidsread.out', 'r') as idsread:
            totalidsread = idsread.read().split()
        with open('newpostidsread.out', 'a') as idsread:
            for line in postid:
                if line in totalidsread:
                    continue
                newcomments = commentfrompost(line)
                idsread.write(line)
                dbh = c['commentdb']
                for comment in newcomments:
                    if commentssaved > 15000:
                        return
                    dbh.nextcomments.insert(comment)#dbh.comments.insert(comment)
                    commentssaved += 1
                print("Total number of comments saved: " + str(dbh.nextcomments.find({}).count()))# str(dbh.comments.find({}).count()))`

if __name__ == '__main__':
    main()
