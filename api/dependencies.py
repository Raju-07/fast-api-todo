from fastapi import status,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from core.config import secret_key,algorithm

oauth_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth_schema))  -> str:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentail",
        headers={"WWW-AUTHENTICATE" : "Bearer"}
        )
    
    try:
        payload = jwt.decode(token,str(secret_key),algorithms=[algorithm])
        username = payload.get("sub")
        if username is None:
            raise credential_exception
    except jwt.PyJWTError:
        raise credential_exception
    
    return username