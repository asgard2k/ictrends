import json

CONFIG = None

# keys in config.json
KEY_SUBREDDITS = "subreddits"
KEY_DURATION = "duration"
KEY_MAX_COUNT = "max_count"
KEY_MAX_COMMENT_LEVEL = "max_comment_level"

def loadConfig():
    with open("config.json", "r") as f:
        global CONFIG
        CONFIG = json.load(f)

loadConfig()