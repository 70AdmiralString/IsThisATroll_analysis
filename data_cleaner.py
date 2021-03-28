import praw

def redditor_cleaner(redditor: praw.models.reddit.redditor.Redditor) -> dict:
	"""
	This function "cleans" the reddit user data.
	The input is 'redditor', an instance of the redditor class.
	The output will:
		1) Provide as much data from 'redditor' as possible.
		2) Omitting any attributes that are not usefule to us (such as redditor.is_friend)
		3) Change the type of certain attributes (such as changing redditor.icon_img from url string to bool)
	The output should also be in a usable form, such a list, dict, or custom object.
	"""

	#Example
	dic = {}
	dic['comment_karma'] = redditor.comment_karma
	return dic


import secrets

reddit = praw.Reddit(
	client_id=secrets.client_id,
	client_secret=secrets.client_secret,
	password=secrets.password,
	user_agent=secrets.user_agent,
	username=secrets.username,
)

redditor = reddit.redditor("spez")
print('Fetched:', redditor._fetched)
if redditor._fetched:
	print('Here are all the attributes of the redditor class')
	print(vars(redditor))
#print('\n The help function will also show most of the methods and "import" attributes', help(redditor))