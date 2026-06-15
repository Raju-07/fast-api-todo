#temp imports
from datetime import date,timedelta
import random

#Project imports
from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session

# Requirements imports
from todo_model import TodoSchema,Priority
from database import engine,LocalSession,get_db,project_url,anon_key,supabase_url
import database
import db_todo_model

# DB Connections imports
import asyncio
from contextlib import asynccontextmanager
from supabase import AsyncClient

# handling function if db changes detected
def handle_db_changes(payload):
    print(" [DATABASE CHANGE EVENT DETECTED]")
    change_data = payload.get('data', {})
    event_enum = change_data.get('type')  
    event_name = event_enum.value if event_enum else "UNKNOWN"
    table_name = change_data.get('table')
    

    row_data = change_data.get('record')
    
    print(f"Action:     {event_name}")
    print(f"Table:      {table_name}")
    print(f"Row Values: {row_data}")
    print("--\n", flush=True)

# lifespan event hook
@asynccontextmanager
async def app_lifespan(app:FastAPI):
    if project_url and anon_key:
        database.supabase_client = await database.acreate_client(project_url,anon_key)
        

        # Configure it to listen to changes and check subscription status
        channel = database.supabase_client.channel("realtime-todo-tracking")

        print("attemping to establishing Realtime Websocket Handshake")

        await (
        channel.on_postgres_changes(
            event="*",  
            schema="public",
            table="todo",
            callback=handle_db_changes
        ).subscribe(
            # Adding a status callback to verify the websocket state!
            lambda status, error=None: print(f" Channel Status: {status}", f"| Error: {error}" if error else "")
            )
        )
        await asyncio.sleep(0.5)
        print("Real-time Event channels open successfully..")
    else:
        print("Realtime Configuration skipped due to missing project url")
    
    yield
    
    print("Clearning application resources..")


app = FastAPI(lifespan=app_lifespan)
db_todo_model.Base.metadata.create_all(bind=engine)


# temperary data insertion 
today =date.today()
def get_exp_date():
    return today + timedelta(days=random.randint(1,20))

# existing data
todos = [    
TodoSchema( title="Learn FastAPI", description="Start FastAPI tutorial", priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),
TodoSchema( title="Read Pydantic", description="Read Pydantic docs",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),
TodoSchema( title="Write tests", description="Write unit tests",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),
TodoSchema( title="Build API", description="Create endpoints",priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),
TodoSchema( title="Add auth", description="Implement auth",priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),
TodoSchema( title="Docs", description="Document API",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="CI/CD", description="Set up CI pipeline",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Debug", description="Fix reported bugs",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Refactor", description="Refactor codebase",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Optimize", description="Performance improvements",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Deploy", description="Deploy to staging",priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Monitor", description="Add monitoring",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Feedback", description="Collect user feedback",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Bugfix", description="Critical bugfix",priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Upgrade deps", description="Update dependencies",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Cleanup", description="Remove unused code",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Analytics", description="Add analytics",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="UX", description="Improve UX",priority=Priority.low,    expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Scale", description="Horizontal scaling",priority=Priority.high,   expired_at=get_exp_date(),is_completed=random.choice([True,False])),    
TodoSchema( title="Release", description="Prepare release notes",priority=Priority.medium, expired_at=get_exp_date(),is_completed=random.choice([True,False]),)]

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


@app.get('/')
def get_todos(db: Session = Depends(get_db),):
    db_todos = db.query(db_todo_model.Todo).all()
    return db_todos

@app.get("/todos/{id}")
def get_todo_by_id(id:int,db: Session = Depends(get_db)):
    todo = db.query(db_todo_model.Todo).filter(db_todo_model.Todo.id == id).first()
    if not todo:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Requrested Todo not Found with {id = }")
    
    return todo
    

# Adding data
@app.post("/todo",status_code=status.HTTP_201_CREATED)
def add_todo(todo:TodoSchema,db: Session = Depends(get_db)):
    try:
        new_todo = db_todo_model.Todo(**todo.model_dump())
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return {'status':"success",'message':'Todo item recorded successfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
        
@app.put("/todo/{id}")
def update_todo(id:int,todo:TodoSchema,db: Session = Depends(get_db)):
    db_todo = db.query(db_todo_model.Todo).filter(db_todo_model.Todo.id == id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Todo Found with {id = } ")

    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.priority = todo.priority
    db_todo.is_completed = todo.is_completed
    db.commit()
    return {'status':'success','message':f"todo updated with {id = }"}

@app.delete("/todo/{id}")
def delete_todo(id:int,db: Session = Depends(get_db)):
    db_todo = db.query(db_todo_model.Todo).filter(db_todo_model.Todo.id == id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Todo Found to delete")
    
    db.delete(db_todo)
    db.commit()
    return {'status':'sucess','message':f'Todo with {id = } deleted successfully'}
    

