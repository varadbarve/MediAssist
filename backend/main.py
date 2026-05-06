from fastapi import FastAPI
from app.core.config import PROJECT_NAME, API_V1_STR
from app.api.v1.api import api_router

from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base
from app.db.session import engine

from fastapi.staticfiles import StaticFiles
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=PROJECT_NAME)

# Ensure temp_calls exists and serve it
if not os.path.exists("temp_calls"):
    os.makedirs("temp_calls")
app.mount("/temp_calls", StaticFiles(directory="temp_calls"), name="temp_calls")


# Set all origins enabled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to {PROJECT_NAME}"}

app.include_router(api_router, prefix=API_V1_STR)

# To run this application:
# 1. Make sure all dependencies from requirements.txt are installed.
# 2. Create a .env file with your API keys (see .env.example).
# 3. From the `backend` directory, run: uvicorn app.main:app --reload