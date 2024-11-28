from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_REVIEW_TTL
from app.services.utils import get_unique_review_key
from redis.asyncio import Redis
from typing import Any


redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

async def save_dict_as_hash(redis_key, dictionary):
    await redis_client.hset(redis_key, mapping=dictionary)
    await redis_client.expire(redis_key, REDIS_REVIEW_TTL)


async def load_dict_as_hash(redis_key):
    redis_data = await redis_client.hgetall(redis_key)
    if redis_data:
        await redis_client.expire(redis_key, REDIS_REVIEW_TTL)
    return redis_data


async def cashing(all_data:dict[str, str], prompt:str, repo_url:str|Any, review:str):
    owner, repo = str(repo_url).split("/")[-2:]
    clear_review = review.replace("    ", "").replace("  ", " ")
    unique_review_key = get_unique_review_key(all_data, prompt)
    await save_dict_as_hash(f"{owner}:{repo}", {unique_review_key: clear_review})


async def get_cashed_data(all_data:dict[str, str], prompt:str, repo_url:str|Any) -> str:
    owner, repo = str(repo_url).split("/")[-2:]

    unique_review_key = get_unique_review_key(all_data, prompt)

    cashed_repo_content = load_dict_as_hash(f"{owner}:{repo}")
    review = (await cashed_repo_content).get(unique_review_key)
    return review


async def close_connection():
    await redis_client.aclose()


async def clear_all_cash():
    await redis_client.flushall()
