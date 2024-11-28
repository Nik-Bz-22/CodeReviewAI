from app.services.github_service import fetch_repository_files
from app.endpoints.loggers.init_logging import logger
from app.models.request_models import ReviewRequest
from app.services.AI_service import analyze_code
from fastapi import APIRouter, HTTPException
import json

router = APIRouter()

@router.post("/")
async def review_code(request: ReviewRequest):
    try:
        github_repo_url = str(request.github_repo_url)
        repo_data = await fetch_repository_files(github_repo_url)

        review_result = await analyze_code(
            repo_data, request.assignment_description, request.candidate_level, github_repo_url
        )
        logger.info("Code review is sending")
        return {"review": json.loads(review_result)}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
