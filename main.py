from datetime import date,timedelta
from fastapi import FastAPI,Depends
from todo_model import Todo,Priority
from database import engine,LocalSession
import db_todo_model
from sqlalchemy.orm import Session
from sqlalchemy import Date
import random

app = FastAPI()
db_todo_model.Base.metadata.create_all(bind=engine)

# temperary data insertion 
today =date.today()
def get_exp_date():
    return today + timedelta(days=random.randint(1,20))

# existing data
todos = [    
Todo( title="Learn FastAPI", description="Start FastAPI tutorial", priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),
Todo( title="Read Pydantic", description="Read Pydantic docs",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),
Todo( title="Write tests", description="Write unit tests",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),
Todo( title="Build API", description="Create endpoints",priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),
Todo( title="Add auth", description="Implement auth",priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),
Todo( title="Docs", description="Document API",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="CI/CD", description="Set up CI pipeline",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Debug", description="Fix reported bugs",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Refactor", description="Refactor codebase",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Optimize", description="Performance improvements",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Deploy", description="Deploy to staging",priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Monitor", description="Add monitoring",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Feedback", description="Collect user feedback",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Bugfix", description="Critical bugfix",priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Upgrade deps", description="Update dependencies",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Cleanup", description="Remove unused code",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Analytics", description="Add analytics",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="UX", description="Improve UX",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Scale", description="Horizontal scaling",priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
Todo( title="Release", description="Prepare release notes",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False]),)]

#function to add existing data to the database
def db_init():
    db = LocalSession()
    try:
        count = db.query(db_todo_model.Todo).count()
        if count == 0:
            for to_do in todos:
                db.add(db_todo_model.Todo(**to_do.model_dump()))
                db.commit()
    finally:
        db.close()

db_init()

#database 
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()



@app.get('/')
def get_todos(db: Session = Depends(get_db)):
    db_todos = db.query(db_todo_model.Todo).all()
    return db_todos

@app.get("/todos/{id}")
def get_todo_by_id(id:int,db: Session = Depends(get_db)):
    todo = db.query(db_todo_model.Todo).filter(db_todo_model.Todo.id == id).first()
    if todo:
        return todo
    return "Todo not Found"

# Adding data
@app.post("/todo")
def add_todo(todo:Todo,db: Session = Depends(get_db)):
    try:
        db.add(db_todo_model.Todo(**todo.model_dump()))
        db.commit()
        return "Todo added.."
    except Exception as e:
        return f"Error: {e}"
        
@app.put("/todo")
def update_todo(id:int,todo:Todo,db: Session = Depends(get_db)):
    db_todo = db.query(db_todo_model.Todo).filter(db_todo_model.Todo.id == id).first()
    if db_todo:
            db_todo.title = todo.title
            db_todo.description = todo.description
            db_todo.priority = todo.priority
            db_todo.is_completed = todo.is_completed
            db.commit()
            return f"todo updated with {id = }"
    return f"No todo found to update with {id = }"

@app.delete("/todo")
def delete_todo(id:int,db: Session = Depends(get_db)):
    db_todo = db.query(db_todo_model.Todo).filter(db_todo_model.Todo.id == id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return "Todo Deleted successfully..."
    else:
        return "Nothing found to delete"

