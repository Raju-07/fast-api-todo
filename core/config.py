import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("PROJECT_SECRET_KEY")
algorithm = os.getenv("ALGORITHM","HS256")
access_token_expire_minutes = os.getenv("ACESS_TOKEN_EXPIRE_MINUTES",20)

