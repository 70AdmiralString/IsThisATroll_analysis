import praw
import secrets
import pandas as pd
import time
from shutil import move
from os import path

reddit = praw.Reddit(
	client_id=secrets.client_id,
	client_secret=secrets.client_secret,
	password=secrets.password,
	user_agent=secrets.user_agent,
	username=secrets.username,
)

class time_keeper(object):
	"""docstring for time_keeper"""
	def __init__(self):
		pass

	def start_time(self, message = ''):
		if message: print(message)
		self.TIME = time.time()

	def end_time(self, message = ''):
		duration = int(time.time() - self.TIME)
		secs = duration
		mins = 0
		hours = 0
		if secs > 60:
			mins = secs // 60
			secs = secs % 60
		if mins > 60:
			hours = mins // 60
			mins = mins % 60
		if message: print(message)
		print('hours', hours, 'mins', mins, 'secs', secs)

	def check_time(self):
		return time.time() - self.TIME

x = time_keeper()

'''
x.start_time()
df_submissions = pd.read_pickle('data_warehouse/2017TransparencyReport/submissions.pkl.zip')
x.end_time('Done loading data_warehouse/2017TransparencyReport/submissions.pkl.zip')
'''

#df_submissions = df_submissions.drop_duplicates()

DataFrame = pd.core.frame.DataFrame
praw_api = praw.reddit.Reddit

def load_df(file_path):
	x = time_keeper()
	x.start_time()
	df = pd.read_pickle(file_path)
	x.end_time('Done loading ' + file_path + ' duration:')
	return df


def save_file(df, file_path, compression = None):
	if compression == None:
		df.to_pickle(file_path)
	if compression == 'zip':
		df.to_pickle(file_path, compression = 'zip')
	else:
		print('Error!')

def backup_file(file_path, second_file_path):
	if path.exists(file_path):
		move(file_path, second_file_path)

def update_df(df: DataFrame, reddit: praw_api, save_time: int, update_time: int, stop_time: int, file_path: str, second_file_path: str, compression = None) -> DataFrame:
	"""updates a database and makes sure that all the items are fetched"""

	#Calculate total unfetched objects
	filt = df['reddit_object'].apply(lambda x: not x._fetched)
	Total = len(df[filt])
	print('we have', Total, 'objects to fetch')

	#total elapsed time
	y = time_keeper()
	y.start_time()

	#time between updates
	x = time_keeper()
	x.start_time()

	#time between saves
	z = time_keeper()
	z.start_time()

	fetched_count = 0
	Index = df.index
	for i in Index:
		[call, label, obj] = df.loc[i]
		if not obj._fetched:
			try:
				obj._fetch()
				df.loc[i] = [call, label, obj]
				fetched_count += 1
			except:
				sub_rdt = str(obj.subreddit)
				print('some error occured on', i, 'in subreddit', sub_rdt)

		#Update
		if x.check_time() > update_time:
			x.start_time()
			remaining = Total - fetched_count
			print(remaining, 'out of', Total, 'remain')
			y.end_time('file has been running for')

		#Save
		if z.check_time() > save_time:
			z.start_time()
			print('SAVING to', file_path)

			#make a backup copy since the saving can take a along time and it errases the existing file
			backup_file(file_path, second_file_path)

			#saves the file and compresses it if needed
			save_file(df, file_path, compression = compression)
			z.end_time('saving took this much time:')
			z.start_time()

		#circut breaker
		if y.check_time() > stop_time:
			print('Timed out. Final save now')
			break

	backup_file(file_path, second_file_path)
	save_file(df, file_path, compression = compression)

	print('fetched', fetched_count, 'out of', Total, 'items')
	y.end_time('Total time')

	return df

#x.start_time()

'''
file_path = 'data_warehouse/2017TransparencyReport/updated_submissions.pkl.zip'
second_file_path = 'data_warehouse/2017TransparencyReport/updated_submissions_copy.pkl.zip'
df = load_df(file_path)

df_updated = update_df(df, reddit, 300, 60, 3600, file_path, second_file_path, compression = 'zip')
'''
#x.end_time()

