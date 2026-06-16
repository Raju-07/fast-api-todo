from database import get_db
from fastapi import Depends,HTTPException,status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from db.schemas import UserResponse,CreateUser
from sqlalchemy.orm import Session
from db.user_modal import UserModal
from db import user_modal
from core.security import hash_password,verify_password,create_access_token 

router = APIRouter(prefix='/auth',tags=["Authentication"])

@router.post("/register/",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register_user(user: CreateUser, db: Session = Depends(get_db)):
    username = db.query(
        user_modal.UserModal).filter(
            user_modal.UserModal.username == user.username).first()
    
    if username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken."
            )
    
    email = db.query(
        user_modal.UserModal).filter(
            user_modal.UserModal.email == user.email
        ).first()
    
    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered."
            )
    

    hashed_password = hash_password(user.password)

    new_user = user_modal.UserModal(
        username= user.username,
        email = user.email,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModal).filter(UserModal.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password")
    
    access_token = create_access_token(data={'sub':str(user.id)})
    return {'access_token':access_token,'token_type':'bearer'}