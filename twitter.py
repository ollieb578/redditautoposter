from __future__ import print_function
import praw, time, random, re, tweepy, requests, md5, os, fileinput

history = ''#history file
subs = []#list of subreddits

CONSUMER_KEY = ''#enter tweepy keys into these fields
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

image_url = ''

def get_content():
    global posts, titles
    posts = []
    titles = []

    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='')#praw id, secret key, and user agent name

    subselect = random.choice(subs)
    print (subselect)
    for submission in reddit.subreddit(subselect).hot(limit=10):
        posts.append(submission.url)
        titles.append(submission.title)

    return posts, titles

def download(i):
    session = requests.session()
    response = session.get(image_url)
    global filename
    filename = 'poster_%s.jpeg' % md5.new(image_url).hexdigest()

    with open(filename, 'wb') as handle:
        for block in response.iter_content(1048576):
            if not block:
                break
            handle.write(block)
        handle.close()
    return filename

def contentgen(i):
    postno = random.randint(0, 9)
    global image_url, title
    image_url = posts[postno]
    title = titles[postno]
    return image_url, title

    check = 0
    check =+ 1

    if check >= 10:
        check = 0
        subselect = random.choice(subs)
        print (subselect)
        for submission in reddit.subreddit(subselect).hot(limit=15):
            posts.append(submission.url)
            titles.append(submission.title)

    return image_url, title

def validate(i):
    contentgen(image_url)

    history = open("", "r")#history file
    used = history.read()
    history.close()

    while not re.search("(.jpg|.png|.gif|.jpeg)$",image_url):
        contentgen(image_url)

    while re.search(image_url,used):
        contentgen(image_url)

    while len(title) >= 140:
        contentgen(image_url)

    download(image_url)

    while os.stat(filename).st_size >= 3000000:
        contentgen(image_url)
        os.remove(filename)
        download(image_url)

    return image_url

def cleanup():
    day = time.strftime('%d')
    day = int(day) - 2
    day = str(day)
    month = time.strftime('%m')
    date = "".join([day,month])

    for line in fileinput.input('', inplace=True):
        if date in line:
            continue
        print(line, end='')

def main():
    get_content()
    validate(image_url)

    api.update_with_media(filename, status=title + "")
    print (image_url)

    history = open("", "a")#history file
    history.write(image_url + '             ' + time.strftime("%d%m") + "\n")
    history.close()

    cleanup()
    time.sleep(10)
    os.remove(filename)

try:
    main()
except:
    main()