"""
Original code: https://gist.github.com/dangayle/4e6864300b58fee09ce1
"""

import sys
from datetime import datetime, timedelta, timezone
import praw
import logging

user_agent = "hot test 1.0 by /u/dangayle"
r = praw.Reddit(user_agent=user_agent)

class SubredditLatest(object):
    """Get all available submissions within a subreddit newer than x."""

    def __init__(self, subreddit, dt, max_count=100, max_comments_level=2):

        # master list of all available submissions
        self.total_list = []

        # subreddit must be a string of the subreddit name (e.g., "soccer")
        self.subreddit = subreddit

        # dt must be a utc datetime object
        self.dt = dt

        # Reddit maximum limit
        self.max_count = max_count

        self.max_comments_level = max_comments_level

    def __call__(self):
        self.get_submissions()
        return self.total_list

    def get_submissions(self, paginate=False):
        # We fetch Submissions by batches of 100
        limit_per_request = 100

        if paginate is True:
            try:
                # get limit of items past the last item in the total list
                submissions = r.subreddit(self.subreddit).new(limit=limit_per_request, params={"after": self.total_list[-1].fullname})
            except IndexError as err:
                logging.error(str(err))
                return
        else:
            submissions = r.subreddit(self.subreddit).new(limit=limit_per_request)

        submissions_list = [
            # iterate through the submissions generator object
            x for x in submissions
            # add item if item.created_utc is newer than an hour ago
            if (self.dt is None) or (datetime.fromtimestamp(x.created_utc, tz=timezone.utc) >= self.dt)
        ]
        # We fetch in batches of limit_per_request, but do we need all of them to meet the max_count?
        add_count = min(limit_per_request, self.max_count - len(self.total_list))
        self.total_list += submissions_list[:add_count]

        # if max_limit is not already reached, and you've hit the limit in current batch, 
        # recursively run this function again to get all of the available items
        if (len(self.total_list) < self.max_count) and (len(submissions_list) == limit_per_request):
            self.get_submissions(paginate=True)
        else:
            return

if __name__ == '__main__':
    an_hour_ago = datetime.now(timezone.utc) - timedelta(hours=24)
    print(SubredditLatest("wallstreetbets", an_hour_ago)())