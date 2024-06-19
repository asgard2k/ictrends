from subreddit_latest import SubredditLatest
from datetime import datetime, timedelta, timezone
import logging
import argparse
import Post
import json
import csv
import praw
import config

RUN_TEST_CODE = True

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s"
    )
    logging.debug("Start of program")

    var = config['subreddits']

    if RUN_TEST_CODE:
        user_agent = "hot test 1.0 by /u/dangayle"
        r = praw.Reddit(user_agent=user_agent)

        with open("C:\workspaces_python\wsb-main\PythonScraper\output.json", "r") as f:
            data = json.load(f)

        # Convert JSON to Python object
        posts = [Post.Post.fromDict(x) for x in data]

        redditor = r.redditor("Dangerous_Turn9787")

        # time_filter can be 'week', 'day', 'year', 'month' or 'all'
        for submission in redditor.submissions.top(time_filter="week"):
            print(submission.title)

        # print("num_comments", submission.num_comments)
        # url = "https://www.reddit.com/r/wallstreetbets/comments/1dhonhu/i_hope_my_17yr_old_self_enjoyed_that_27/"
        # submission = r.submission(url=url)
        # print("num_comments", submission.num_comments)
        # counter = 0

        # comments = [Post.Comment(x) for x in submission.comments if isinstance(x, praw.models.reddit.comment.Comment)]
        # print("processed comments count", len(comments))
        # for top_level_comment in submission.comments:
        #     if isinstance(top_level_comment, MoreComments):
        #         continue
        #     counter = counter + 1
        #     print(top_level_comment.body)

        # print("processed comments count", submission.num_comments)

    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("file", help="file path to write posts to", type=str)
        parser.add_argument(
            "--duration",
            help="duration in hours. for example, 1 would be last 1 hour of posts. -1 means all posts",
            type=int,
        )
        parser.add_argument("--max_count", help="maximum posts to retrieve", type=int)
        parser.add_argument(
            "--max_comments_level",
            help="1 for top-level comments only, 2 for top-level and immedidate replies, and so on",
            type=int,
        )
        args = parser.parse_args()

        if args.duration is None:
            args.duration = config.CONFIG[config.KEY_DURATION]
        if args.max_count is None:
            args.max_count = config.CONFIG[config.KEY_MAX_COUNT]
        if args.max_comments_level is None:
            args.max_comments_level = config.CONFIG[config.KEY_MAX_COMMENT_LEVEL]

        logging.debug("Loading tickers.csv")
        stockTickers = {}
        with open("tickers.csv", mode="r") as infile:
            reader = csv.reader(infile)
            for row in reader:
                stockTickers[row[0].split(",")[0]] = {}

        logging.debug("Retrieve Reddit submissions")
        n_hours_ago = (
            None
            if args.interval <= 0
            else datetime.now(timezone.utc) - timedelta(hours=args.interval)
        )
        submissions = SubredditLatest(
            "wallstreetbets",
            dt=n_hours_ago,
            max_count=args.max_count,
            max_comments_level=args.max_comments_level,
        )()

        # Convert submissions to Post objects
        converted_posts = [Post.Post(x) for x in submissions]
        print("processed post count", len(converted_posts))

        with open(args.file, "w") as f:
            json.dump(converted_posts, f, default=lambda o: o.__dict__, indent=4)

    logging.debug("End of program")
