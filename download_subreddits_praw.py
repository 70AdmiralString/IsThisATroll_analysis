import praw
import secrets
import pandas as pd

reddit = praw.Reddit(
	client_id=secrets.client_id,
	client_secret=secrets.client_secret,
	password=secrets.password,
	user_agent=secrets.user_agent,
	username=secrets.username,
)

from subreddit_comment_dic import target_subreddits
from subreddit_submission_dic import target_post_subreddits

subs1 = list(set(target_subreddits))
subs2 = list(set(target_post_subreddits))
subs1 += subs2
subs = list(set(subs1))
df = pd.DataFrame(columns = ['display_name', 'subreddit_object'])
df.index.name = 'id_hash'
i = 0
errs = 0
for sub in subs:
	try:
		subrddt = reddit.subreddit(sub)
		print(subrddt.display_name, i)
		id_hash = subrddt.name
		display_name = subrddt.display_name
		df.loc[id_hash] = [display_name, subrddt]
		i +=1
		#if i>10:
		#	break
	except:
		print('some weird error occured')
		errs +=1
		print(errs, ' total errors have occured')

df.to_pickle('data_warehouse/subreddit_data.pkl')

