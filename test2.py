import sys
from datetime import datetime, timedelta
import praw

user_agent = "hot test 1.0 by /u/dangayle"
r = praw.Reddit(user_agent=user_agent)

limit = 1000  # Reddit maximum limit
total_list = []
submissions = r.subreddit('wallstreetbets').new(limit=limit, time_filter='all')
submissions_list = [
    x for x in submissions
    #if datetime.utcfromtimestamp(x.created_utc) >= an_hour_ago
]
total_list += submissions_list
if len(submissions_list) == limit:
    submissions = r.subreddit('wallstreetbets').new(
        # get limit of items past the last item in the total list
        limit=100, params={"after": total_list[-1].fullname}
    )
submissions_list_2 = [
    # iterate through the submissions generator object
    x for x in submissions
    # add item if item.created_utc is newer than an hour ago
    if datetime.utcfromtimestamp(x.created_utc) >= an_hour_ago
]
total_list += submissions_list_2
print(total_list)