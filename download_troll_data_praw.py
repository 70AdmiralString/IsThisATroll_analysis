import praw
import secrets

reddit = praw.Reddit(
	client_id=secrets.client_id,
	client_secret=secrets.client_secret,
	password=secrets.password,
	user_agent=secrets.user_agent,
	username=secrets.username,
)

from troll_list import Trolls
import pandas as pd
import datetime

USER = False

if USER:
	df = pd.DataFrame(columns = ['id', 'user_name', 'redditor_object', 'data_set', 'last_pulled', 'total_karma'])

	i = 0
	for troll in Trolls:
		obj = reddit.redditor(troll)
		try:
			id_num = obj.id
			karma = obj.total_karma
			time = datetime.datetime.now()
			data_set = '17TrnspRprt'
			df.loc[i] = [id_num, troll, obj, data_set, time, karma]
			print(troll, 'index = ', i)
		except:
			print('redditor', troll, 'index', i, 'cannot be pulled')

		i+= 1
		#if i > 10: break

	df.to_pickle("data_warehouse/user_data.pkl")

df = pd.DataFrame(columns = ['post_id', 'user_name', 'user_id', 'submission_object', 'subreddit', 'subreddit_id', 'url', 'data_set', 'created', 'last_pulled', 'score'])

i = 0
j = 0
k = 0
for troll in Trolls:
	user = reddit.redditor(troll)
	j += 1
	if j > 10: break
	try: 
		user_id = user.id
		data_set = '17TrnspRprt'
		username = troll
		print(j, troll)
		i = 0

		for post in user.submissions.top(limit = 100):
			i += 1
			try:
				submission_object = post
				subreddit = post.subreddit.display_name
				subreddit_id = post.subreddit.id
				url = post.permalink
				post_id = post.id
				created = post.created_utc
				score = post.score
				df.loc[k] = [post_id, username, user_id, submission_object, subreddit, subreddit_id, url, data_set, created, datetime.datetime.now(), score]
				print('entry:', k)
				k += 1
			except:
				print('post', i, 'of user', j, 'not found')
	except:
		print('user', j, troll, 'not found')

df.to_pickle("data_warehouse/post_data.pkl")