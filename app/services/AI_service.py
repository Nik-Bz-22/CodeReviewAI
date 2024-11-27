from ..config import GEMINI_API_KEY, MAIN_PART_OF_PROMPT
from .redis_service import cashing, get_cashed_data
from .utils import extract_json_from_string
import google.generativeai as genai
import asyncio


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

async def analyze_code(repo_data: dict, description: str, level: str, github_repo_url:str):
    try:
        prompt = (
            f"{MAIN_PART_OF_PROMPT}"
            f"Task description: {description}. "
            f"Candidate level: {level}. "
            f"Repository content: {repo_data}."
        )
        if cashed_data := await get_cashed_data(all_data=repo_data, prompt=prompt, repo_url=github_repo_url):
            return cashed_data

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, model.generate_content, [prompt])
        if data := response.parts.pop(0).text:
            review_dict = extract_json_from_string(data)
            await cashing(all_data=repo_data, prompt=prompt, repo_url=github_repo_url, review=review_dict)
            return review_dict
        else:
            return "No content in the response."
    except Exception as e:
        raise RuntimeError(f"Error analyzing code through gemini: {str(e)}")
