# core/security.py
import jwt
import bcrypt
from datetime import datetime, timezone, timedelta
from core.config import secret_key, algorithm, access_token_expire_minutes

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes,salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Convert both strings to bytes so bcrypt can safely compare them
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=float(access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, str(secret_key), algorithm)