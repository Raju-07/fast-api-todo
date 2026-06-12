from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from supabase import AsyncClient,acreate_client
from dotenv import load_dotenv
from typing import Optional
import os

#loading env file to the environment
load_dotenv()

#global supabase client
supabase_client: Optional[AsyncClient] = None

supabase_url = os.getenv("DB_URL")
project_url = os.getenv("PROJECT_URL")
anon_key = os.getenv("ANON_KEY")


if supabase_url is None:
    raise RuntimeError("DB connection url is None")

# setup sync engine for slqalchemy endpoints
engine = create_engine(url=supabase_url,pool_pre_ping=True)
LocalSession = sessionmaker(bind=engine,autoflush=False,autocommit=False)

# DB Dependency for route injection
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


