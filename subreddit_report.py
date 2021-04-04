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
#n = len(Trolls)

def get_post(sub):
	"""Get's the url of posts that we want"""
	i = 900
	for user in Trolls:
		user = Trolls[i]
		if i >= 1000:
			break
		i += 1
		print('i = ', i)
		troll = reddit.redditor(user)
		for post in troll.submissions.top(limit = 100):
			try:
				if post.subreddit.display_name == sub:
					print('subreddit:', post.subreddit.display_name)
					print('poster:', user)
					print('permalink', post.permalink)
					print('url:', post.url)
			except:
				print('Maybe a 403 error')

import time

def print_report(sub, start = None, stop = None, verbose = True):
	"""
	prints the full report for this subreddit
	Returns the number of posts, num of comments, 
	number of distinct users posting/commenting,
	top poster/commenter,
	num of comments with bigger score than 5, num of posts with bigger score than 5
	urls for some comments and posts
	"""
	start_time = time.time()
	posts = {}
	comms = {}
	top_post = '' #url
	bottom_post = ''
	mid_post = ''
	max_post_score = -100
	min_post_score = 100
	top_comment = ''
	bottom_comment = ''
	mid_comment = ''
	max_comment_score = -100
	min_comment_score = 100
	most_posts = '' #user
	most_comments = ''
	n = len(Trolls)
	if start == None:
		print('start is none')
		start = 0
	if stop == None:
		print('end is none')
		stop = n
	stop = min(n, stop)
	mid = int((stop-start)/3) + start
	search_com = False
	search_post = False

	for i in range(start, stop):
		user = Trolls[i]
		i += 1
		if i >= stop:
			break
		if i == mid:
			search_com = True
			search_post = True
		if verbose: print('user no.', i, 'username:', user)
		troll = reddit.redditor(user)
		try:
			for post in troll.submissions.top(limit = 100):
				try:
					if post.subreddit.display_name == sub:
						if search_post:
							if verbose: print('found mid post')
							mid_post = post.permalink
							search_post = False
						if user not in posts:
							posts[user] = 1
						else:
							posts[user] += 1
						if (max_post_score < post.score):
							max_post_score = post.score
							top_post = post.permalink
							if verbose: print('new top post')
						if (min_post_score > post.score):
							min_post_score = post.score
							bottom_post = post.permalink
							if verbose: print('new bottom post')
				except:
					print('maybe a 403 error')
		except: 
			print('this is a slippery troll')
		try:
			for comm in troll.comments.new(limit = 100):
				try:
					if comm.subreddit.display_name == sub:
						if search_com:
							if verbose: print('found mid comment')
							mid_comment = comm.permalink
							search_com = False
						if user not in comms:
							comms[user] = 1
						else:
							comms[user] += 1
						if (max_comment_score < comm.score):
							max_comment_score = comm.score
							top_comment = comm.permalink
							if verbose: print('new top comment')
						if (min_comment_score > comm.score):
							min_comment_score = comm.score
							bottom_comment = comm.permalink
							if verbose: print('new bottom comment')
				except:
					print('maybe a 403 error')
		except:
			print('this is a slippery troll')

	print('Report for subreddit', 'r/' + sub)
	print('Total posts:', sum(posts.values()))
	print('No. of unique posters:', len(posts.values()))
	print('Top post (score of', max_post_score, '):', top_post)
	print('Bottom post (score of', min_post_score, '):', bottom_post)
	print('Random post:', mid_post)
	print('All posters:', posts)
	print('Total comments:', sum(comms.values()))
	print('No. of unique commentors:', len(comms.values()))
	print('Top comment (score of', max_comment_score, '):', top_comment)
	print('Bottom comment (score of', min_comment_score, '):', bottom_comment)
	print('Random comment:', mid_comment)
	print('All commentors:', comms)

	elapsed_time = int(time.time() - start_time)
	mins = elapsed_time // 60
	secs = elapsed_time % 60

	print('Compiling the report took:', mins, 'mins', secs, 'secs')



