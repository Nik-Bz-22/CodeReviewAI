from ..config import GITHUB_TOKEN, GIT_DOWNLOAD_LIMIT
from typing import List, Dict
import asyncio
import base64
import httpx

from ..endpoints.loggers.init_logging import logger


def to_clear_git_api_response(api_response) -> str:
    file_meta_info = api_response.json()
    encoded_file_content = file_meta_info.get("content")

    try:
        clear_content = base64.b64decode(encoded_file_content).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        logger.info(exc)
        raise ValueError("Error decoding base64 content.") from exc

    return clear_content


async def get_file_content(owner: str, repo_name: str, file_path: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}"
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        api_response = await client.get(url, headers=headers)
        api_response.raise_for_status()

        clear_content = to_clear_git_api_response(api_response)

        return clear_content

async def get_directory_contents(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    response.raise_for_status()
    return response.json()

async def fetch_repository_files_list(repo_url: str) -> List[Dict]:
    owner, repo = str(repo_url).split("/")[-2:]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"

    async with httpx.AsyncClient() as client:
        all_files = []

        async def process_directory(directory_url: str):
            items = await get_directory_contents(client, directory_url)
            tasks = []
            for item in items:
                if item["type"] == "file":
                    all_files.append(item)
                elif item["type"] == "dir":
                    tasks.append(process_directory(item["url"]))
            await asyncio.gather(*tasks)

        await process_directory(api_url)
        return all_files

async def fetch_repository_files(repo_url: str) -> Dict[str, str]:
    data = await fetch_repository_files_list(repo_url)
    owner, repo = str(repo_url).split("/")[-2:]
    all_data = {}

    semaphore = asyncio.Semaphore(GIT_DOWNLOAD_LIMIT)

    async def fetch_content(file_info):
        async with semaphore:
            path = file_info["path"]
            content = await get_file_content(owner, repo, path)
            return path, content

    tasks = [fetch_content(file_info) for file_info in data]
    results = await asyncio.gather(*tasks)
    for result in results:
        all_data[result[0]] = result[1]

    logger.info(f"Data fetched for {owner}/{repo}")
    return all_data
