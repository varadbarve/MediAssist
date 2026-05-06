from fastapi import FastAPI
from app.core.config import PROJECT_NAME, API_V1_STR
from app.api.v1.api import api_router

app = FastAPI(title=PROJECT_NAME)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to {PROJECT_NAME}"}

app.include_router(api_router, prefix=API_V1_STR)

# To run this application:
# 1. Make sure all dependencies from requirements.txt are installed.
# 2. Create a .env file with your API keys (see .env.example).
# 3. From the `backend` directory, run: uvicorn app.main:app --reload