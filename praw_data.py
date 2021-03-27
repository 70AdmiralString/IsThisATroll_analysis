"""
How to access the Python Reddit Api Wrapper (PRAW)
"""
import praw

"""
To do anything with praw, you need to instanciate an instance of the Reddit class.
But to actually pull anything from the internet we need to register with reddit.
I know, it is stupid.
I've already done it for us, but here's how to do it in the future.

1) Get a reddit account

username: XXXXXXXXXXXXX
password: XXXXXXXXXXXXX

2) Register the 'app'

a) Go to https://www.reddit.com/prefs/apps/ 
b) Click "create an app"
c) Enter a name for your "app"
d) Select "script" if your app is not going to post anything or reddit.
e) Enter "http://localhost:8080" under "redirect uri"
f) Hit "Create App"

3) Instanciate Reddit

Enter the following python code

The client ID is the 14-character string listed just under “personal use script” for the desired developed application

The client secret is at least a 27-character string listed adjacent to secret for the application.

"""
import secrets

reddit = praw.Reddit(
	client_id=secrets.client_id,
	client_secret=secrets.client_secret,
	password=secrets.password,
	user_agent=secrets.user_agent,
	username=secrets.username,
)

print('You are now using:', reddit.user.me())

'''
for submission in reddit.subreddit("learnpython").hot(limit=10):
	print(submission.title)
'''

# assume you have a reddit instance bound to variable `reddit`
subreddit = reddit.subreddit("redditdev")

# assume you have a Reddit instance bound to variable `reddit`
redditor2 = reddit.redditor("Spez")
print(redditor2.link_karma)
# Output: u/bboe's karma

print("User Information")
for attr in redditor2.__dict__:
	print(attr, ':', redditor2.__dict__[attr])

print("\n Comment Information")
for i in redditor2.comments.new(limit = 1): comment = i
for attr in comment.__dict__:
	print(attr, ':', comment.__dict__[attr])
