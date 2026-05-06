from fastapi import FastAPI
from app.core.config import PROJECT_NAME, API_V1_STR
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.db.base import Base
from app.db.session import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=PROJECT_NAME)

# 1. ADD MIDDLEWARE FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. ENSURE FOLDER EXISTS
if not os.path.exists("temp_calls"):
    os.makedirs("temp_calls")

# 3. MOUNT STATIC FILES
app.mount("/temp_calls", StaticFiles(directory="temp_calls"), name="temp_calls")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to {PROJECT_NAME}"}

app.include_router(api_router, prefix=API_V1_STR)