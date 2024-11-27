import os
from dotenv import load_dotenv

load_dotenv()

MAIN_PART_OF_PROMPT =f"Analyze this code from the repository and return the review result (text) in the following format: Found files(key=files), downsides, comments, rating(key=rating)(0-10), conclusion. Write the entire answer in dictionary format from Python. That is, each heading (item) will be a key, and the content will be a value. don't write anything else. the answer should be similar to the json.loads(your_answer) method"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0

