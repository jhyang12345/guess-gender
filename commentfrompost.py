import facebook, requests, sys, pickle
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from getgender import checkvalidity


totalcomments = 0

mytoken = ''
with open('mytoken.txt', 'r') as token:
    mytoken = token.read().strip()

graph = facebook.GraphAPI(access_token=mytoken, version='2.3')

count = 0
def getname(user):#need to query user again
    try:
        user = graph.get_object(id=user['id'], connection_name="user")
        return user['name']
    except:
        return ''
    return ''


def commentfrompost(postid, dbh):
    checkurl = ''
    post = None
    try:
        print(postid)
        mytoken = ''
        with open('mytoken.txt', 'r') as token:
            mytoken = token.read().strip()
        graph = facebook.GraphAPI(access_token=mytoken, version='2.3')
        post = graph.get_object(id=postid, connection_name="post")
    except:
        print("Error returning False!")
        return []
    comments = None
    ret = []
    print("Trying postid: " + postid)
    try:
        comments = post['comments']
        print("Comments found!")
    except:
        return []
    for x in range(100):
        newurl = ''
        try:
            newurl = comments['paging']['next']
        except:
            newurl = "None here"
            break

        for comment in comments['data']:
            try:
                if comment['message'] != None and checkvalidity(getname(comment['from']), comment['message']):
                    if(dbh.nextcomments.find({'id': comment['id'].strip()}).count() > 0):
                        return []
                    if(len(comment['message']) >= 20):
                        print(comment['message'])
                        addcomment = {}
                        addcomment['id'] = comment['id'].strip()
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
            print("Connected successfully")
        except ConnectionFailure as e:
            sys.stderr.write("Connection failed.")
            sys.exit(1)
        dbh = c['commentdb']
        totalidsread = []
        with open('newpostidsread.out', 'r') as idsread:
            totalidsread = idsread.read().split()
        with open('newpostidsread.out', 'a') as idsread:
            for line in postid:
                line = line.strip()
                if line.strip() in totalidsread:
                    print("Skipping", line)
                    continue
                newcomments = commentfrompost(line, dbh)
                if(newcomments == False):
                    continue
                if newcomments != []:
                    idsread.write(line + '\n')

                for comment in newcomments:
                    if commentssaved > 100000:
                        return
                    if dbh.nextcomments.find({'id': comment['id']}).count() < 1:
                        dbh.nextcomments.insert(comment)#dbh.comments.insert(comment)
                        commentssaved += 1
                print("Total number of comments saved: " + str(dbh.nextcomments.find({}).count()))# str(dbh.comments.find({}).count()))`

if __name__ == '__main__':
    main()
