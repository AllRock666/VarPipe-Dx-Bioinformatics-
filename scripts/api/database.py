import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pymongo import MongoClient

# PostgreSQL Setup
PG_URL = os.getenv("DATABASE_URL", "sqlite:///./varpipe_test.db") # Fallback to sqlite for dev
engine = create_engine(PG_URL, connect_args={"check_same_thread": False} if "sqlite" in PG_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MongoDB Setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
try:
    mongo_client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000)
    mongo_db = mongo_client["varpipe_dx"]
    annotations_collection = mongo_db["annotations"]
except Exception as e:
    print(f"Warning: MongoDB not reachable at {MONGO_URL}. Mocking collection.")
    annotations_collection = None
