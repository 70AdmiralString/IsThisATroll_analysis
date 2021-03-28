import praw
import secrets #where we keep the loggin info

reddit = praw.Reddit(
	client_id=secrets.client_id,
	client_secret=secrets.client_secret,
	password=secrets.password,
	user_agent=secrets.user_agent,
	username=secrets.username,
)

print('You are now logged in as:', reddit.user.me(), '\n')

#Cannot fetch Redditors
redditor1 = reddit.redditor("spez")
print('Redditor was fetched:', redditor1._fetched)
print('Get any item. link_karma:', redditor1.link_karma)
print('Redditor was fetched:', redditor1._fetched)

#Cannot fetch Subreddits
subreddit1 = reddit.subreddit("redditdev")
print('Subreddit was fetched:', subreddit1._fetched)
print('Get any item. description:', subreddit1.description[:20])
print('Subreddit was fetched:', subreddit1._fetched)


#Can fetch Submissions
submission1 = reddit.submission(id="39zje0")
print('Submission was fetched:', submission1._fetched)
print('Get any item. title:', submission1.title)
print('Submission was fetched:', submission1._fetched)

#Can fetch Comments
comment1 = reddit.comment(id='cswg4ku')
print('Comment was fetched:', comment1._fetched)
print('Get any item. body:', comment1.body[:20])
print('Comment was fetched:', comment1._fetched)
