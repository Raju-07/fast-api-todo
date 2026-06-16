from fastapi import HTTPException,status
import db_todo_model
from db_todo_model import Todo
from sqlalchemy.orm import Session
from todo_model import TodoSchema
from datetime import date


async def get_all_todo(db: Session):
    todos = db.query(Todo).all()
    return todos

async def get_todo_by_id(id: int,db: Session):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo not found with {id = }")

    return todo

async def add_todo(todo:TodoSchema,db: Session):
    try:
        new_todo = db_todo_model.Todo(**todo.model_dump())
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return {'status':"success",'message':'Todo item recorded successfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
        
async def update_todo(id:int,todo:TodoSchema,db: Session):
    db_todo = db.query(db_todo_model.Todo).filter(db_todo_model.Todo.id == id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Todo Found with {id = } ")

    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.priority = todo.priority
    db_todo.is_completed = todo.is_completed
    db.commit()
    return {'status':'success','message':f"todo updated with {id = }"}

async def delete_todo(id:int,db: Session):
    db_todo = db.query(db_todo_model.Todo).filter(db_todo_model.Todo.id == id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Todo Found to delete")
    
    db.delete(db_todo)
    db.commit()
    return {'status':'sucess','message':f'Todo with {id = } deleted successfully'}

async def update_expired_time(id:int,db:Session,data = date.today(),):
    db_data = db.query(db_todo_model.Todo).filter(db_todo_model.Todo.id == id).one()
    if not db_data:
        return HTTPException(status_code=(status.HTTP_404_NOT_FOUND),detail="No Data found to update")
    db_data.expired_at = data
    db.commit()
    return {'status':'success','message':f' Date updated where {id = }'}
