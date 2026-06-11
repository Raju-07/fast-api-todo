from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
db_url_supabase = os.getenv("DB_URL")

if db_url_supabase is None:
    raise RuntimeError("DB_URL environment variable is not set")

db_url = "postgresql://postgres:12345678@localhost:5432/todos"
engine = create_engine(url=db_url_supabase)
LocalSession = sessionmaker(autocommit=False,autoflush=False,bind=engine)