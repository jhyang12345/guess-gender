import facebook, requests

mytoken = ''
with open('mytoken.txt', 'r') as token:
    mytoken = token.read().strip()

graph = facebook.GraphAPI(access_token=mytoken, version='2.2')

post = graph.get_connections(id='walmart', connection_name="posts")

def printmessage(post):
    for message in post['data']:
        if 'message' in message:
            print(message['message'].encode('utf-8'))

def getpostsfrompage(page):#pass name of page
    ret = []
    post = graph.get_connections(id=page, connection_name="posts")
    postcount = 0
    for x in range(500):
        post = requests.get(post['paging']['next']).json()
        for ids in post['data']:
            if 'id' in ids:
                ret.append(ids['id'].encode('utf-8'))
                postcount += 1
                print("Number of posts found: " + str(postcount))
    return ret

"""
for x in range(10):
    try:
        post = requests.get(post['paging']['next']).json()
        printmessage(post)
    except KeyError:
        break
"""
def findgroupbyname(name):
    checkurl = 'https://graph.facebook.com/search?q='\
     + name + '&type=group&access_token=' + mytoken
    group = requests.get(checkurl).json()
    return group['data']['id']

def iteratethroughpages():
    with open('newpagename.in', 'r') as f:
        for line in f:
            savelist = getpostsfrompage(line.strip())
            print("Scaping posts from page: " + line.strip())
            with open('newpostids.in', 'a') as writefile:
                for x in savelist:
                    writefile.write(x.decode('utf-8') + '\n')
                writefile.close()
#findgroupbyname('codingeverybody')
iteratethroughpages()
