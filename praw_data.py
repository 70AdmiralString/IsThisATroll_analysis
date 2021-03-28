import praw
import secrets

reddit = praw.Reddit(
	client_id=secrets.client_id,
	client_secret=secrets.client_secret,
	password=secrets.password,
	user_agent=secrets.user_agent,
	username=secrets.username,
)

print('You are now using:', reddit.user.me(), '\n')

'''
for submission in reddit.subreddit("learnpython").hot(limit=10):
	print(submission.title)
'''

import pprint

def print_attrs(obj):
	"""prints the attributes"""

	for attr in obj.__dict__:
		result = obj.__dict__[attr]
		if type(result) == str:
			n = len(result)
			n = min(n, 100)
			if n == 100:
				print(attr, ':', obj.__dict__[attr][:n], '...')
		else:
			print(attr, ':', obj.__dict__[attr])
	

def subreddit_attrs(example = "redditdev"):
	"""Prints a list of all attributes of the subreddit object, using the example subreddit"""

	obj = reddit.subreddit(example)
	temp = obj.description
	print('Attributes for the Subreddit:', example)
	print_attrs(obj)

def redditor_attrs(example = "spez"):
	"""Prints a list of all attributes of the redditor object, using the example redditor"""

	obj = reddit.redditor(example)
	temp = obj.link_karma
	print('Attributes for the Redditor:', example)
	print_attrs(obj)

def comment_attrs(example = "cs8llxd"):
	"""Prints a list of all attributes of the comment object, using the example comment"""

	obj = reddit.comment(id = example)
	temp = obj.body
	print('Attributes for the Comment: id =', example)
	print_attrs(obj)

def submission_attrs(example = "39zje0"):
	"""Prints a list of all attributes of the submission object, using the example submission"""

	obj = reddit.submission(id = example)
	temp = obj.title
	print('Attributes for the Submission:', obj.title)
	print_attrs(obj)

