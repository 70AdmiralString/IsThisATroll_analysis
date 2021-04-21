import praw
import pandas as pd
import secrets

reddit = praw.Reddit(
	client_id=secrets.client_id,
	client_secret=secrets.client_secret,
	password=secrets.password,
	user_agent=secrets.user_agent,
	username=secrets.username,
)

stored_subreddit_data = pd.read_pickle("./data_warehouse/subreddit_data.pkl")
stored_submission_data = pd.read_pickle("./data_warehouse/post_data.pkl.zip")
stored_comment_data = pd.read_pickle("./data_warehouse/comment_data.pkl.zip")
stored_redditor_data = pd.read_pickle("./data_warehouse/user_data.pkl")


def redditor_cleaner(redditor: praw.models.Redditor) -> dict:
	"""
	This function "cleans" the reddit user data.
	The input is 'redditor', an instance of the redditor class.
	The output will:
		1) Provide as much data from 'redditor' as possible.
		2) Omitting any attributes that are not usefule to us (such as redditor.is_friend)
		3) Change the type of certain attributes (such as changing redditor.icon_img from url string to bool)
	The output should also be in a usable form, such a list, dict, or custom object.
	"""

	#Example
	dic = {}
	dic['comment_karma'] = redditor.comment_karma
	return dic

class StorageError(Exception):
    '''
        An exception to be raised specifically when an object that should be in the local database is not present.
    '''
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
        
def get_from_local_database(object_id):
    '''
        Goes into the local database and finds the corresponding object with id object_id.
        Object_id is a string corresponding to the id of the object.  The first three characters indicate the type.
            t1_ : Comment
            t2_ : Redditor
            t3_ : Submission
            t5_ : Subreddit
       
        Returns the object, or raises an error if it cannot be found in the database.
    '''
    type_string = object_id[0:3]
    if type_string == "t1_":
        data = stored_comment_data
        if object_id in data.comment_id.values:
            result = data[data.comment_id == object_id]
        else:
            raise StorageError(object_id, "This data is not in local storage.")
        
    elif type_string == "t2_":
        data = stored_redditor_data
        if object_id[3:] in data.id.values:
            result = data[data.id == object_id[3:]]
        else:
            raise StorageError(object_id, "This data is not in local storage.")
        
    elif type_string == "t3_":
        data = stored_submission_data
        if object_id[3:] in data.post_id.values:
            result = data[data.post_id == object_id[3:]]
        else:
            raise StorageError(object_id, "This data is not in local storage.")
            
    elif type_string == "t5_":
        data = stored_subreddit_data
        try:
            result = data.loc[object_id].subreddit_object
        except KeyError:
            raise StorageError(object_id, "This data is not in local storage.")
            
    else:
        raise ValueError("Invalid id data_type")
    
    return result

def get_subreddit_by_name(subreddit_name : str, stored : bool):
    '''
        Outputs a Subreddit object, given the subreddit's name as info 
            - needed as submissions only contain the name of the subreddit, not the id.
        
        stored is a boolean which indicates whether the id should be looked for in the local database (if True)
            or if it should be looked for online (if False)
    '''
    if stored:
        data = stored_subreddit_data
        if subreddit_name in data["display_name"].values:
            result = data[data["display_name"] == subreddit_name]
            result = result.subreddit_object.values[0]
        else:
            raise StorageError(subreddit_name, "This data is not in local storage.")
    else:
        result = reddit.subreddit(subreddit_name)
   
    return result

def subreddit_info(subreddit : praw.models.Subreddit, stored : bool) -> dict:
    '''
        Outputs a dictionary consisting of all of the necessary information to be kept about a 
        subreddit in the form of a single dictionary with keys which are the relevant attributes.
        
        Given the subreddit object as input
        
        stored is a boolean which indicates whether the id should be looked for in the local database (if True)
            or if it should be looked for online (if False)
    '''
    result = {}
    attr_to_keep = ["description","name","display_name","over18","subscribers"]
    for attr in attr_to_keep:
        result[attr] = subreddit.__dict__[attr]
    return result

def get_submission_by_id(submission_id : str, stored: bool):
    '''
        Outputs a Submission object, given the submission's id as info.
        
        stored is a boolean which indicates whether the id should be looked for in the local database (if True)
            or if it should be looked for online (if False)
    '''
    if stored:
        submission = get_from_local_database(submission_id).submission_object.values[0]
    else:
        submission = reddit.submission(submission_id[3:])
        
    return submission

def submission_info(submission : praw.models.Submission, stored : bool) -> dict:
    '''
        Outputs a dictionary consisting of all of the necessary information to be kept about a 
        submission in the form of a single dictionary. 
        This includes the data on the subreddit containing the submission, with such attributes having a "subreddit" prepended to them.
        
        stored is a boolean which indicates whether the id should be looked for in the local database (if True)
            or if it should be looked for online (if False)
    '''
    result = {}
    subreddit = get_subreddit_by_name(submission.subreddit.display_name, stored)
    subreddit_result = subreddit_info(subreddit, stored)
    for attr in subreddit_result:
        result["subreddit " + attr] = subreddit_result[attr]
    
    attr_to_keep = ['created_utc', 'edited', 'is_original_content', 'is_self','link_flair_text','num_comments', \
                    'over_18', 'permalink', 'score', 'selftext', 'title', 'upvote_ratio', 'url']
    #TODO: Include other attributes that were removed to make the code work
    # poll_data was removed as not all submissions had it as an attribute
    for attr in attr_to_keep:
        result[attr] = submission.__dict__[attr]
      
    return result

def get_comment_by_id(comment_id : str, stored : bool):
    '''
        Outputs a Comment object, given the comment's id as info.
        
        stored is a boolean which indicates whether the id should be looked for in the local database (if True)
            or if it should be looked for online (if False)
    '''
    if stored:
        comment = get_from_local_database(comment_id).comment_object.values[0]
    else:
        comment = reddit.comment(comment_id[3:])
        
    return comment
    
    
def comment_info(comment : praw.models.Comment, stored : bool) -> dict:
    '''
        Outputs a dictionary consisting of all of the necessary information to be kept about a 
        comment in the form of a single dictionary. 
        This includes the data on the submission containing the comment, with such attributes 
            having a "submission" prepended to them.
        This includes the data on the subreddit containing the comment, with such attributes 
            having a "submission subreddit" prepended to them.
        
        stored is a boolean which indicates whether the id should be looked for in the local database (if True)
            or if it should be looked for online (if False)
    '''        
    result = {}
    submission = get_submission_by_id(comment.submission.name, stored)
    submission_result = submission_info(submission, stored)
    for attr in submission_result:
        result["submission " + attr] = subreddit_result[attr]
    
    attr_to_keep = ['body', 'created_utc', 'edited', 'is_submitter', 'link_id', 'permalink', 'score']
    for attr in attr_to_keep:
        result[attr] = submission.__dict__[attr]
      
    return result

def get_redditor_by_name(redditor_username : str, stored : bool):
    '''
        Outputs a redditor object, given the redditor's username as info.
        
        stored is a boolean which indicates whether the id should be looked for in the local database (if True)
            or if it should be looked for online (if False)
    '''
    if stored:
        data = stored_redditor_data
        if redditor_username in data["user_name"].values:
            redditor = data[data["user_name"] == redditor_username]
            redditor = redditor.redditor_object.values[0]
        else:
            raise StorageError(subreddit_name, "This data is not in local storage.")
    else:
        redditor = reddit.redditor(redditor_username)
        
    return redditor

def redditor_info(redditor : praw.models.Redditor, comment_limit : int, submission_limit : int, stored : bool) -> dict:
    '''
        Outputs a dictionary consisting of all of the necessary information to be kept about a 
        comment in the form of a single dictionary. 
        Most of the keys of this dictionary will simply be attributes of the Redditor, with the value
            meaning the value of that attribute.
        The "comments" key will have a value which is a list of dictionaries containing the relevant
            information on each comment.
        The "submissions" key will do likewise for each submission.
        The "subreddits" key will do likewise for each user subreddit.
            #TODO - Implement the subreddits part of this - currently not implemented.
            
        comment_limit and submission_limit are integers which represent the number of posts of each type which should be considered
            #TODO Have a more robust system for comment limit and submission limit selection, or a way to not always just pick the top ones.
            
        stored is a boolean which indicates whether the id should be looked for in the local database (if True)
            or if it should be looked for online (if False)
    '''        
    result = {}
    
    result["comments"] = []
    for comment in redditor.comments.top(limit = comment_limit):
        result["comments"].append(comment_info(comment, stored))
    
    result["submissions"] = []
    for submission in redditor.submissions.top(limit = submission_limit):
        # Need to exclude cases of removed posts
        if submission.subreddit.display_name != "u_reddit":
            result["submissions"].append(submission_info(submission, stored))
    
    attr_to_keep = ["comment_karma", "created_utc", "has_verified_email", "is_mod", "link_karma", "name", "subreddit"]
    for attr in attr_to_keep:
        result[attr] = submission.__dict__[attr]
        
    return result

























