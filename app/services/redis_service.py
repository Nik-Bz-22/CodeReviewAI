from redis.asyncio import Redis
from typing import Any
import asyncio
from app.services.utils import get_unique_review_key
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB


redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

async def set_value(key: str, value: str, expire: int = None):
    await redis_client.set(key, value, ex=expire)

async def get_value(key: str):
    return await redis_client.get(key)



async def save_dict_as_hash(redis_key, dictionary):
    await redis_client.hset(redis_key, mapping=dictionary)


async def load_dict_as_hash(redis_key):
    return await redis_client.hgetall(redis_key)



async def save_set(redis_key, set_to_save):
    await redis_client.sadd(redis_key, *set_to_save)

async def load_set(redis_key):
    return await redis_client.smembers(redis_key)


async def close_connection():
    await redis_client.aclose()


async def cashing(all_data:dict[str, str], prompt:str, repo_url:str|Any, review:str):
    owner, repo = str(repo_url).split("/")[-2:]
    unique_review_key = get_unique_review_key(all_data, prompt)
    await save_dict_as_hash(f"{owner}:{repo}", {unique_review_key: review})

async def get_cashed_data(all_data:dict[str, str], prompt:str, repo_url:str|Any) -> str:
    owner, repo = str(repo_url).split("/")[-2:]

    unique_review_key = get_unique_review_key(all_data, prompt)

    cashed_repo_content = load_dict_as_hash(f"{owner}:{repo}")
    review = (await cashed_repo_content).get(unique_review_key)
    return review


if __name__ == '__main__':

    async def f():
        # await set_value("foo", json.dumps({"a": 1, "b": 2}))
        # print((json.loads(await get_value("foo"))))
        # await close_connection()
        # await save_dict_as_hash(
        #     "name1",
        #     {
        #                 "hash": "5528c7a41820292eba1d99719a7eb74c09708f09bfa8f57837983e6d64e4cc3a",
        #                 "reviews": {
        #                      ("first", "prompt"): "first review",
        #                      ("second", "prompt"): "second review"
        #                 }
        #             }
        #     )
        # data = await load_dict_as_hash("name1")
        # print(data["reviews"][('first', 'prompt1')])
        # await get_value("name")
        # await save_set("data_set", (1,2,3,4,5,6,1,1,1,1,1,1,1,1))
        # print(await load_set("data_set"))
        # await cashing({"file1": "content1","file2": "content2","file3": "content","file4": "content4"}, ("оцени от 1 до 10", "и опиши код"), "https://github.com/Nika/SCA", "Я оцениваю это на 7 из 10.")
        # print([print(i) for i in (await load_dict_as_hash("Nik-Bz-22:SCA"))])
        # data = await get_cashed_data({"file1": "content1","file2": "content2","file3": "content","file4": "content4"}, ("оцени от 1 до 10", "и опиши код"), "https://github.com/Nika/SCA")
        # print(data)
        await redis_client.flushall()
        async for key in redis_client.scan_iter("*"):  # Асинхронный перебор
            print(f"Key: {key}")
        await close_connection()
    asyncio.run(f())