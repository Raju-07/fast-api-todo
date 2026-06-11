from enum import Enum
from datetime import date
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy import Date

class Priority(int,Enum):
    high = 1
    medium = 2
    low = 3

class Todo(BaseModel):
    title: str   
    description: str 
    priority: int = 2
    expired_at: Annotated[date,"Number of days after expiration"]
    is_completed: bool = False
    


