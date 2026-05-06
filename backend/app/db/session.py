from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core import config

# SQLite specific argument for multi-threaded FastAPI access
connect_args = {"check_same_thread": False} if config.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    config.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
