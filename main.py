#temp imports
from datetime import date,timedelta
import random

#Project imports
from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware

# Requirements imports
from todo_model import TodoSchema,Priority
from database import engine,LocalSession,get_db,project_url,anon_key,supabase_url
import database
import db_todo_model
import db.user_modal

# DB Connections imports
import asyncio
from contextlib import asynccontextmanager
from supabase import AsyncClient

from api.dependencies import get_current_user
from api.auth import router as auth_router

import crud

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


app = FastAPI(
    lifespan=app_lifespan,
    title="Todo Application",
    version="1.0.0",
    description="This is a project where i'm making a todo apis to understand the fastapi better",)

db_todo_model.Base.metadata.create_all(bind=engine)
db.user_modal.Base.metadata.create_all(bind=engine)

app.include_router(auth_router,prefix='/api/v1')

@app.get("/api/v1/protected-data")
async def get_secure_data(current_user: str = Depends(get_current_user)):
    return {'message':f"from {current_user = } you've access to this data "}

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["PUT","GET","POST","DELETE"],
    allow_headers = ["*"],
)

@app.get('/')
async def get_todos(db: Session = Depends(get_db)):
    return await crud.get_all_todo(db=db)

@app.get("/todos/{id}")
async def get_todo_by_id(id:int,db: Session = Depends(get_db)):
    return await crud.get_todo_by_id(id,db=db)    

# Adding data
@app.post("/todo",status_code=status.HTTP_201_CREATED)
async def add_todo(todo:TodoSchema,db: Session = Depends(get_db)):
    return await crud.add_todo(todo,db=db)        

@app.put("/todo/{id}")
async def update_todo(id:int,todo:TodoSchema,db: Session = Depends(get_db)):
   return await crud.update_todo(id,todo,db=db)

@app.delete("/todo/{id}")
async def delete_todo(id:int,db: Session = Depends(get_db)):
    return await crud.delete_todo(id,db=db)

@app.patch("/todo/{id}")
async def update_expired_time(id:int,db: Session = Depends(get_db)):
    await crud.update_expired_time(id,db=db)


