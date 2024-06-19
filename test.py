import pmaw
import datetime as dt

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
new_list = [print(val, index) for (index, val) in enumerate(my_list) if val % 2 == 0]


# reddit = pmaw.PushshiftAPI()
# after = int(dt.datetime(2023,9,1,0,0).timestamp())
# before = int(dt.datetime(2023,9,30,23,59).timestamp())
# limit = 100
# subreddit = 'wallstreetbets'

# posts = reddit.search_submissions(subreddit=subreddit, limit=1000)
# post_list = [post for post in posts]

# comments = reddit.search_comments(subreddit=subreddit, limit=limit, before=before, after=after)

# for comment in comments:
#     print(comment.body)
