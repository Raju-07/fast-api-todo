from enum import Enum
from datetime import date
from pydantic import BaseModel

class Priority(int,Enum):
    high = 1
    medium = 2
    low = 3

class Todo(BaseModel):
    id: int
    title: str
    description: str
    priority: Priority
    created_at: date
    


