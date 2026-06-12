from enum import Enum
from datetime import date
from pydantic import BaseModel,Field
from typing import Annotated

class Priority(int,Enum):
    high = 1
    medium = 2
    low = 3

class TodoSchema(BaseModel):
    title: str   = Field(max_length=250,description="The Title of the Task")
    description: str = Field(max_length=255,description="Brief detail about the task")
    priority: int = Field(default=Priority.medium,description="1=High, Medium=2,Low=3")
    expired_at: date = Field(description="Date when task End")
    is_completed: bool = False

    class Config:
        from_attributes = True
    


