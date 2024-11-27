from fastapi import FastAPI
from app.endpoints.review import router as review_router


app = FastAPI(title="CodeReviewAI")

app.include_router(review_router, prefix="/review")
