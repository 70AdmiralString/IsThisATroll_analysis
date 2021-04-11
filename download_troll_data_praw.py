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