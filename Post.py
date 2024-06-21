from Utils import remove_emoji, unmark
import praw
from praw.models import MoreComments

# Keys for the Post dictionary
KEY_NAME = 'name'
KEY_AUTHOR = 'author'
KEY_AUTHOR_ID = 'author_id'
KEY_TITLE = 'title'
KEY_ID = 'id'
KEY_URL = 'url'
KEY_TEXT = 'text'
KEY_SUBREDDIT = 'subreddit'
KEY_CREATED_UTC = 'created_utc'
KEY_COMMENTS = 'comments'
KEY_PERMALINK = 'permalink'
KEY_NUM_COMMENTS = 'num_comments'

# Keys for the Comment dictionary
KEY_BODY = 'body'
KEY_REPLIES = 'replies'

class Post:
    def __init__(self, id, name, author_id, author, title, url, permalink, text, subreddit, created_utc, num_comments, comments):
        self.id =id
        self.name = name
        self.author = author
        self.author_id = author_id
        self.title = title
        self.id = id
        self.permalink = permalink
        self.url = url
        self.text = text
        self.subreddit = subreddit
        self.created_utc = created_utc
        self.num_comments = num_comments
        self.comments = comments

    @classmethod
    def fromSubmission(cls, praw_submission):
        return Post(
            id=praw_submission.id,
            name=praw_submission.name,
            author_id=praw_submission.author.id,
            author=praw_submission.author.name,
            title=praw_submission.title,
            url=praw_submission.url,
            permalink=praw_submission.permalink,
            text=remove_emoji(praw_submission.selftext),
            subreddit=praw_submission.subreddit.display_name,
            created_utc=praw_submission.created_utc,
            num_comments=praw_submission.num_comments,
            comments=[Comment.fromComment(x) for x in praw_submission.comments if isinstance(x, praw.models.reddit.comment.Comment)]
            ) 

    @classmethod
    def fromDict(cls, post_dict):
        comments = [Comment.fromDict(x) for x in post_dict[KEY_COMMENTS] if post_dict[KEY_COMMENTS] is not None and len(post_dict[KEY_COMMENTS]) > 0]
        return Post(
            id=post_dict[KEY_ID],
            name=post_dict[KEY_NAME],
            author_id=post_dict[KEY_AUTHOR_ID],
            author=post_dict[KEY_AUTHOR],
            title=post_dict[KEY_TITLE],
            url=post_dict[KEY_URL],
            permalink=post_dict[KEY_PERMALINK],
            text=post_dict[KEY_TEXT],
            subreddit=post_dict[KEY_SUBREDDIT],
            created_utc=post_dict[KEY_CREATED_UTC],
            num_comments=post_dict[KEY_NUM_COMMENTS],
            comments=comments
            )

class Comment:
    def __init__(self, body, replies):
        # The original body is markdown formatted. We want to remove the formatting.
        self.body = body
        # Get the replies. It is in a CommentForest.
        self.replies = None
        # replies = comment.replies
        # if replies is not None:
        #     self.replies = [Comment(reply) for reply in replies if isinstance(reply, praw.models.reddit.comment.Comment)]
        # else:
        #     self.replies = None

    @classmethod
    def fromComment(cls, praw_comment):
        tmp = None
        replies = praw_comment.replies
        if replies is not None:
            tmp = [Comment.fromComment(reply) for reply in replies if isinstance(reply, praw.models.reddit.comment.Comment)]
        return Comment(
            body=unmark(praw_comment.body),
            replies=tmp
            )
            
    @classmethod
    def fromDict(cls, comment_dict):
        return Comment(body=comment_dict[KEY_BODY], replies=comment_dict[KEY_REPLIES])