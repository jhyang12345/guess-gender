import sys, urllib.request, json, codecs


APP_ID = '1671609293072685'
APP_SECRET = 'f3f5df3d81c7fe709697de1eebc8f102'

def create_post_url(graph_url, APP_ID, APP_SECRET):
    post_args = "/posts/?key=value&access_token=" + APP_ID + "|" + APP_SECRET
    post_url = graph_url + post_args

    return post_url

def main():
    list_companies = ["walmart", "cisco", "pepsi", "facebook"]
    url = "https://graph.facebook.com/"
    for company in list_companies:
        post_url = create_post_url(url + company, APP_ID, APP_SECRET)
        web_response = urllib.request.urlopen(post_url)
        readable_page = web_response.read().decode('utf8')
        reader = codecs.getreader('utf-8')
        json_postdata = json.loads(readable_page)
        json_fbposts = json_postdata['data']

        print(json_fbposts)


if __name__ == '__main__':
    main()
