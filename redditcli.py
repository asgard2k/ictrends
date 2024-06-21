from subreddit_latest import SubredditLatest
from datetime import datetime, timedelta, timezone
import logging
import argparse
import Post
import json
import csv
import praw
import config

RUN_TEST_CODE = False

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO, format=" %(asctime)s -  %(levelname)s -  %(message)s"
    )
    logging.info("Start of program")

    var = config.CONFIG['subreddits']

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

        logging.info("Loading tickers.csv")
        stockTickers = {}
        with open("tickers.csv", mode="r") as infile:
            reader = csv.reader(infile)
            for row in reader:
                stockTickers[row[0].split(",")[0]] = {}

        logging.info("Retrieve Reddit submissions")
        n_hours_ago = (
            None
            if args.duration <= 0
            else datetime.now(timezone.utc) - timedelta(hours=args.duration)
        )
        submissions = SubredditLatest(
            "wallstreetbets",
            dt=n_hours_ago,
            max_count=args.max_count,
            max_comments_level=args.max_comments_level,
        )()

        with open(args.file, "w") as f:
            batch_size = 25
            num_submissions = len(submissions)
            num_processed = 0

            f.write('[\n\t')

            for i in range(0, num_submissions, batch_size):
                logging.info("Processing Iteration %d" % (i / batch_size))
                # Convert submissions to Post objects
                converted_posts = [Post.Post.fromSubmission(x) for x in submissions[i : i + min(batch_size, num_submissions-num_processed)]]
                num_processed += len(converted_posts)
                logging.info("Iteration %d: Processed post count: %d. Total post count: %d" % (i / batch_size, len(converted_posts), num_processed))

                json_string = json.dumps(converted_posts, default=lambda o: o.__dict__, indent=4)

                 # Remove array brackets
                str_start_index = json_string.find('{')
                str_end_index = json_string.rfind('}')
                json_string = json_string[str_start_index:str_end_index+1]

                f.write(json_string)
                f.write(",\n")

                # for post in converted_posts:
                #     json_string = jsonpickle.encode(post)
                #     f.write(json_string)
                #     f.write(",\n")

            f.write(']')

    logging.info("End of program")
