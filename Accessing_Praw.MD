# How to access the Python Reddit Api Wrapper (PRAW)

To do anything with Praw, you need to instanciate an instance of the Reddit class. But to actually pull anything from the internet we need to register with reddit.

I know, it is stupid.

I've already done it for us, but here's how to do it in the future.

## 1. Get a reddit account

username: AAAAAAAAAAAAA
password: BBBBBBBBBBBBB

## 2. Register the 'app'

a) Go to https://www.reddit.com/prefs/apps/ 
b) Click "create an app"
c) Enter a name for your "app"
d) Select "script" if your app is not going to post anything or reddit.
e) Enter "http://localhost:8080" under "redirect uri"
f) Hit "Create App"

## 3. Create a Secrets.py file

Create a file called ``Secrets.py``. You can do this in the same file if you don't care about privacy. 
Enter the following code:
``
client_id="ZZZZZZZZZZZZZ"
client_secret="XXXXXXXXXX"
password="BBBBBBBBBBB"
user_agent="testscript by u/AAAAAAAAAAAAA"
username="AAAAAAAAAAAA"
``
The client ID is the 14-character string listed just under “personal use script” for the desired developed application

The client secret is at least a 27-character string listed adjacent to secret for the application.

Username and Password are your reddit account username and passwords

user_agent is just a string explaining who has made this

## 4. Instanciate Reddit

Enter the following python code

``
import praw
import secrets
reddit = praw.Reddit(
	client_id=secrets.client_id,
	client_secret=secrets.client_secret,
	password=secrets.password,
	user_agent=secrets.user_agent,
	username=secrets.username,
)
``
