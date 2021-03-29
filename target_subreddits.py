#This will be used to find which subreddits are the targets of the most trolls

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
subreddits = {}

n = len(Trolls)
i = 0
for user in Trolls:
	i += 1
	if (i%10 == 0):
		print('troll number', i, 'of', n)
	troll = reddit.redditor(user)
	try:
		for comm in troll.comments.new(limit = 1000):
			sub = comm.subreddit.display_name
			if sub in subreddits:
				subreddits[sub] += 1
			else:
				subreddits[sub] = 1
	except:
		print('Maybe a 403 error occured. We do not have access to this info')

print(n, 'Trolls commented in', len(subreddits.keys()), 'unique subreddits')
subreddits2 = {k: v for k, v in sorted(subreddits.items(), key=lambda item: -item[1])}

#I already did this, no need to do it again
#f = open("subreddi_comment_dic.py", "w")
#f.write('target_subreddits = ' + str(subreddits2))
#f.close()

items = list(subreddits.items())
print(items[:10])
