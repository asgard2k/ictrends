import sys
from datetime import datetime, timedelta
import praw

user_agent = "hot test 1.0 by /u/dangayle"
r = praw.Reddit(user_agent=user_agent)

class SubredditLatest(object):
    """Get all available submissions within a subreddit newer than x."""

    def __init__(self, subreddit, dt):

        # master list of all available submissions
        self.total_list = []

        # subreddit must be a string of the subreddit name (e.g., "soccer")
        self.subreddit = subreddit

        # dt must be a utc datetime object
        self.dt = dt

    def __call__(self):
        self.get_submissions(self)
        return self.total_list

    def get_submissions(self, paginate=False):
        """Get limit of subreddit submissions."""
        limit = 1000  # Reddit maximum limit

        if paginate is True:
            try:
                # get limit of items past the last item in the total list
                submissions = r.subreddit(self.subreddit).new(limit=limit, params={"after": self.total_list[-1].fullname})
            except IndexError:
                logger.exception("param error")
                return
        else:
            submissions = r.subreddit(self.subreddit).new(limit=limit)

        submissions_list = [
            # iterate through the submissions generator object
            x for x in submissions
            # add item if item.created_utc is newer than an hour ago
            if datetime.utcfromtimestamp(x.created_utc) >= self.dt
        ]
        self.total_list += submissions_list

        # if you've hit the limit, recursively run this function again to get
        # all of the available items
        if len(submissions_list) == limit:
            self.get_submissions(paginate=True)
        else:
            return

if __name__ == '__main__':
    an_hour_ago = datetime.utcnow() - timedelta(hours=1)
    print(SubredditLatest("wallstreetbets", an_hour_ago)())