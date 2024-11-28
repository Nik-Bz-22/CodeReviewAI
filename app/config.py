from dotenv import load_dotenv
from typing import Final
import pathlib
import os

load_dotenv()

MAIN_PART_OF_PROMPT = f"""Analyze this code from the repository and return the review result (text) in the following format: 
        Found files(key=files), downsides, comments, rating(key=rating)(0-10), conclusion. 
        Write the entire answer in dictionary format from Python. 
        That is, each heading (item) will be a key, and the content will be a value. 
        Don't write anything else. the answer should be similar to the json.loads(your_answer) method"""

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GIT_DOWNLOAD_LIMIT = 15

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"

IN_DOCKER = os.getenv("IN_DOCKER")

if IN_DOCKER:
    REDIS_HOST = "redis"
    REDIS_PORT = 6379
else:
    REDIS_HOST = "localhost"
    REDIS_PORT = 6380

REDIS_DB = 0
REDIS_REVIEW_TTL = 60 * 60


ROOT_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parents[1]
LOGS_DIR: Final[pathlib.Path] = ROOT_DIR.joinpath("logs")
