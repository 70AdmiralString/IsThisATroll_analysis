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

class StorageError(Exception):
    '''
        An exception to be raised specifi
        y when an object that should be in the local database is not present.
    '''
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class Preclean():
    '''
        This class contains the methods which are used to preclean a data set.  
        
        It has attributes representing the particular data set which it is processing, 
            and representing the information contained in that dataset which is to be kept upon processing.

        Non-class methods gather data using the local database.
        Class methods gather data using praw, or do not need to gather data.
    '''
    # This list simply lists the four valid types of praw models used.
    valid_types = ["redditor", "comment", "submission", "subreddit"]
    # This list contains subreddits with only moderator or meaningless comments, such as
    # notifications that a particular user has been banned.
    subreddits_to_avoid = ["u_reddit"]
    # The following dictionary consists of four parts, in which the key is the name of a type of object
    # and the value is a list of attributes kept by precleaning.
    attrs_to_keep = {"redditor":["comment_karma", "created_utc", "has_verified_email", "is_mod", "link_karma", "name", "subreddit"],\
                     "comment":['body', 'created_utc', 'edited', 'is_submitter', 'link_id', 'permalink', 'score'],\
                     "submission":['created_utc', 'edited', 'is_original_content', 'is_self','link_flair_text','num_comments', \
                                   'over_18', 'permalink', 'score', 'selftext', 'title', 'upvote_ratio', 'url'],\
                     "subreddit":["description","name","display_name","over18","subscribers"]};
    
    def __init__(self, data_set:str = ''):
        '''
            data_set is a string which identifies the name of the dataset
                This also indicates the folder in which the dataset will be.
                If data_set = '', it will be assumed that there is no dataset.
        '''
        self.data_set = data_set
        if data_set != '':
            self.subreddit_data = pd.read_pickle("./data_warehouse/subreddits.pkl")
        
            self.submission_data = pd.read_pickle("./data_warehouse/" + data_set + "/submissions.pkl.zip")
            self.comment_data = pd.read_pickle("./data_warehouse/" + data_set + "/comments.pkl.zip")
            self.redditor_data = pd.read_pickle("./data_warehouse/" + data_set + "/redditors.pkl")

    def get_from_database(self, call:str, object_type:str):
        '''
            This method gets the object with identifier call from the local database for the corresponding object_type
                If
                    object_type is "redditor", then call is the username
                    object_type is "submission", then call is the id (without the t3_)
                    object_type is "comment", then call is the id (without the t1_)
                    object_type is "subreddit", then call is the display_name 
        '''
        if object_type == "redditor":
            database = self.redditor_data
        elif object_type == "submission":
            database = self.submission_data
        elif object_type == "comment":
            database = self.comment_data
        elif object_type == "subreddit":
            database = self.subreddit_data
        else:
            raise StorageError(object_type, "This is not a valid type of data in the database.")
            
        data = database[self.redditor_data['call'] == call]
        if len(data) == 0:
            raise StorageError(call, "This data is not in local storage.")
        return data['reddit_object'].values[0]
    
    '''
        The following class methods gather raw data using praw.
    '''
    @classmethod
    def get_redditor(cls,username:str):
        return reddit.redditor(username)
    
    @classmethod
    def get_submission(cls,submission_id:str):
        return reddit.submission(submission_id)
    
    @classmethod
    def get_comment(cls,comment_id:str):
        return reddit.comment(comment_id)
    
    @classmethod
    def get_redditor(cls,subreddit_name:str):
        return reddit.subreddit(subreddit_name)     
    
    '''
        The following class methods take praw objects and give a list of the subobjects
            of corresponding type which the object contains, or just the subjobject itself if
            it is uniquely specified.

        When necessary, limit_num denotes the number of top-level items to get.
            This applies when selecting redditor comments or submissions.
            TODO: add functionality to select more than just top-level
    '''
    @classmethod
    def redditor_comments(cls,redditor:praw.models.Redditor, limit_num:int):
        return list(redditor.comments.top(limit = limit_num))
                    
    @classmethod
    def redditor_submissions(cls,redditor:praw.models.Redditor, limit_num:int):
        return list(redditor.submissions.top(limit = limit_num))
    
    @classmethod
    def comment_submission(cls,comment:praw.models.Comment):
        return comment.submission
    
    @classmethod
    def comment_subreddit(cls,comment:praw.models.Comment):
        return comment.subreddit
    
    # TODO: Decide whether this method is actually needed at all, or if it should simply be removed.
    # At present it is not used.
    @classmethod
    def comment_parentcomment(cls,comment:praw.models.Comment):
        result = comment.parent()
        if type(result) == praw.models.Comment:
            result.refresh()
            return result
        return None
    
    @classmethod
    def submission_subreddit(cls,submission:praw.models.Comment):
        return submission.subreddit
    
    
    '''
        The following class method gathers all relevant subobjects of every type
            for the specified redditor.
        It finds information on the subobjects using the local database.
        
        comments_limit and submissions_limit are integers representing the number of each to get.
            It's worth noting that fewer of each than this number may appear.
            This happens either because the user has made fewer such posts than the number requested
                or because some of them were made to subreddits which are specifically being excluded
                from the analysis.
        #TODO: find a way to select other than just top
        
    '''
    @classmethod
    def get_subobjects(cls, redditor:praw.models.Redditor, comments_limit:int, submissions_limit:int):
        comments = Preclean.redditor_comments(redditor, comments_limit)
        submissions = Preclean.redditor_submissions(redditor, submissions_limit)        
        submissions = filter(lambda post: Preclean.submission_subreddit(post) \
                             in Preclean.subreddits_to_avoid, submissions)
        
        comments_subobjects = [[comment, Preclean.comment_submission(comment), \
                                Preclean.comment_subreddit(comment)] for comment in comments] 
        submissions_subobjects = [[submission, Preclean.submission_subreddit(submission)] \
                                  for submission in submissions]
        
        return [redditor, comments_subobjects, submissions_subobjects]
                                   
    '''
        The following method takes in a redditor and outputs a list of all subobjects, just as the previous.
        This one, however, does so by taking the previously obtained list, gathering all of the identifying information,
        and looking each entry up in the database.
    '''
    def get_subobjects_from_database(self, redditor:praw.models.Redditor, comments_limit:int, submissions_limit:int):
        subobjects = Preclean.get_subobjects(redditor, comments_limit, submissions_limit)
        
        fun1 = lambda entry: self.get_from_database(entry[0].id,"comment")
        fun2 = lambda entry: self.get_from_database(entry[1].id,"submission")
        fun3 = lambda entry: self.get_from_database(entry[2].display_name,"subreddit")
        comments = map(lambda entry: [fun1(entry), fun2(entry), fun3(entry)],\
                              subobjects[1])
        
        fun4 = lambda entry: self.get_from_database(entry[0].id,"submission")
        fun5 = lambda entry: self.get_from_database(entry[1].display_name,"subreddit")
        submissions = map(lambda entry: [fun4(entry), fun5(entry)],\
                              subobjects[2])
        
        return [redditor, comments, submissions]

    '''
        The following class method takes an object of the specified type and extracts the desired attributes from it.
            object_type should be one of "redditor", "comment", "submission", or "subreddit"
            It is important that object_type match the actual type of the object.
            #TODO: Actually throw an error if these types do not match. - or just check the type instead of having object_type at all.
    '''
    @classmethod
    def preclean_extract(cls, reddit_object, object_type:str) -> dict:
        if object_type not in valid_types:
            raise StorageError(object_type, "This is not a valid type of data.")
        
        attrs = Preclean.attrs_to_keep[object_type]
        result = {}
        for attr in attrs:
            result[attr] = reddit_object.__dict__[attr]
        
        return result

    '''
        The following class method carries out the precleaning procedure on all subobjects
            of a given redditor.
        subobjects is a list of lists of the form
            [redditor, [[comment1, comment_submission1, comment_subreddit1],...],[[submission1,submission_subreddit1],...]
        In particular, it is the output of the get_subobjects or get_subobjects_from_database functions.
        
        The result is a dictionary, see the following function for a more detailed description.
    '''
    @classmethod
    def preclean_extract_subobj(cls, subobjects) -> dict:
        redditor_data = Preclean.preclean_extract(subobjects[0],"redditor")
        
        fun1 = lambda entry: Preclean.preclean_extract(entry[0],"comment")
        fun2 = lambda entry: Preclean.preclean_extract(entry[1],"submission")
        fun3 = lambda entry: Preclean.preclean_extract(entry[2],"subreddit")
        comment_data = map(lambda entry: [fun1(entry), fun2(entry), fun3(entry)], subobjects[1])
        
        fun4 = lambda entry: Preclean.preclean_extract(entry[0],"submission")
        fun5 = lambda entry: Preclean.preclean_extract(entry[1],"subreddit")
        submission_data = map(lambda entry: [fun4(entry), fun5(entry)], subobjects[2])
        
        redditor_data["comments"] = comment_data
        redditor_data["submissions"] = submission_data
        return redditor_data
    
    '''
        The following class method carries out the entire precleaning procedure on a redditor username.
        Given the username, it will ask praw for the redditor object, find all necessary subobjects,
            and then preclean all of that data.
            
        The result is a dictionary where all but two keys have int or str values.
            The remaining two keys, "comments" and "submissions", have values which are lists of dictionaries, 
            corresponding to each of the comments and submissions specified.
            
        comments_limit and submissions_limit are integers telling how many comments or submissions to find
            Fewer than this number may ultimately appear.
    '''
    @classmethod
    def preclean(cls, username:str, comments_limit:int, submissions_limit:int) -> dict:
        redditor = Preclean.get_redditor(username)
        subobjects = Preclean.get_subobjects(redditor, comments_limit, submissions_limit)
        return Preclean.preclean_extract_subobj(subobjects)
    
    '''
        The following method is identical to that above, but uses the database for all lookups at all steps.
    '''
    def preclean_from_database(self, username:str, comments_limit:int, submissions_limit:int) -> dict:
        redditor = self.get_from_database(username, "redditor")
        subobjects = self.get_subobjects_from_database(redditor, comments_limit, submissions_limit)
        return Preclean.preclean_extract_subobj(subobjects)
    
    '''
        The following method carries out the precleaning process for all usernames present in the database.
    '''
    def preclean_all(self, comments_limit:int, submissions_limit:int):
        return [preclean_from_database(username, comments_limit, submissions_limit) \
                for username in self.redditor_data["call"]]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    







