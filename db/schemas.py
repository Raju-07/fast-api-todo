from pydantic import Field,BaseModel,EmailStr


class CreateUser(BaseModel):
    username: str = Field(...,max_length=100,description="Account username")
    email: EmailStr = Field(...,max_length=100,description="Account Email Address")
    password: str = Field(...,max_length=100,description="Use strong Password")

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True