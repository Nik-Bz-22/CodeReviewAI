from app.endpoints.review import router as review_router
from app.endpoints.loggers.init_logging import logger
from fastapi import FastAPI


app = FastAPI(title="CodeReviewAI")
logger.info("Application Started")

app.include_router(review_router, prefix="/review")
