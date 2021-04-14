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

index = pd.MultiIndex.from_tuples([], names = ['Ux', 'Cx'])

df = pd.DataFrame(index = index, columns = ['comment_id', 'author', 'author_id', 'post_id', 'parent_id', 'comment_object', 'subreddit_name', 'permalink', 'data_set', 'created', 'last_pulled', 'score'])

i = 0
j = 0
k = 0

data_set = '17TrnspRprt'

for troll in Trolls:
	user = reddit.redditor(troll)
	j += 1
	#if j > 10: break
	try: 
		author_id = user.id
		author = troll
		print(j, troll)
		i = 0

		for comm in user.comments.top(limit = 1000):
			i += 1
			try:

				comment_id = comm.name
				#author = str(comm.author)
				#author_id = comm.author_fullname
				post_id = comm.link_id
				post_author = comm.link_author
				parent_id = comm.parent_id
				comment_object = comm
				subreddit_name = str(comm.subreddit)
				permalink = comm.permalink
				score = comm.score
				created = comm.created

				last_pulled = datetime.datetime.now()

				df.loc[(j,i),:] = [comment_id, author, author_id, post_id, parent_id, comment_object, subreddit_name, permalink, data_set, created, last_pulled, score]



				k += 1
				print('user:', j, 'comment:', i, 'entry:', k)

				if (k % 100 == 0): df.to_pickle("data_warehouse/scratch.pkl")
			except:
				print('post', i, 'of user', j, 'not found')
		print('User:', j, 'had', i, 'comments')
	except:
		print('user', j, troll, 'not found')

#t1 = comment
#t2 = redditor
#t3 = post
#t5 = subreddit

df.to_pickle("data_warehouse/scratch.pkl.zip", compression="zip")

	#to load the data again, just use df = pd.read_pickle('data_warehouse/post_data.pkl.zip')

"""
The comment data will be bigger than the last one. Maybe 10 times the size. So we need a new method of downloading and storing the data.
I should stratify the trolls, put it into 4 parts. Everyone runs the script on 1 fourth of the trolls (taken using mod 4).
Dumps in batches of 100.
There should be a way to check to see how much "progess" has been made downloading and start from there.

When restarting the program, it will: 1) check which strata you are working in, 2) retrieve all the data already stored, 3) check what the last user/comment was, 4) continue from there.

indexes need to be better organized
"""