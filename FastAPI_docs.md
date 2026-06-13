## FastAPI :

FastAPI is web Framework it's lightweight and blazing fast for handing api work

In this documents i'm not going to include so much theoritical part as we've a dedicated about the theory and all. In this i'll heavily focus on how to connect it with database with sqlalchemy and with the supabase connection string and realtime channel 

### Importance

* **High performance**
* **Type support (python hint)**
* **Data Validation (built in pydantic)**
* **Automatic document Generation (docs,redoc)**
* **Async,Await capabilities**

### Creating first App

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_home():
	return {'message':'Hello,World'}

```


### Connection with Database (localhost) Postgres

For connecting it with database we required sqlalchemy package and psycopg2 postgres driver and from sqlalchemy.orm we need sessionmaker and create_engine from sqlalchemy

and a db url for binding it with the engine and we're needed to create the db manually as the sqlalchemy doesn't create it automatically

URL MUST follow this structure

    `postgresql://username:password@host:port/database_name`

```python
from sqlalchemy import create_engine
from sqlalchemy import sessionmaker

#for postgres db (local)
db_url = "postgresql://postgres:password@localhost:5432/todo"

engine = create_engine(db_url)
local_session = sessionmaker(bind=engine,autocommit=False,autoflush=False	)
```


### Connecting it with Supabase Database

it's so simple to connect with the supabase database as we just need to change the db_url of the project with supabase project connection string 

* create an account on supabase
* create a project under an org
* In the Get connected Section look for Direct Connect: for Connection String
* ![1781365049599](image/FastAPI_docs/1781365049599.png)
* copy the connection string and replace it with the db_url
* congrats you're successfully connected with the supabase database


### Enabling Realtime Connection 

we need to do couple things needed

1. project url of supabase
2. anon key of supabase
3. enable the "realtime" feature of the desired table
4. Enable RLS ("Row level security") for Secure purpose
5. Must create polocy for the table , for "CRUD" operations with role permission carefully

##### Good Practice

add all the credential in the .env file if you haven't yet then create it first and add 

keep it mind to don't push it on the github, as it contain sensitive data '.env' never meant to push on github. and also add this filename in the '.gitignore' file

##### database.py file look like this

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from supabase import AsyncClient,acreate_client
from dotenv import load_dotenv
from typing import Optional
import os

#loading env file to the environment
load_dotenv()

#global supabase client
supabase_client: Optional[AsyncClient] = None

supabase_url = os.getenv("DB_URL")
project_url = os.getenv("PROJECT_URL")
anon_key = os.getenv("ANON_KEY")


if supabase_url is None:
    raise RuntimeError("DB connection url is None")

# setup sync engine for slqalchemy endpoints
engine = create_engine(url=supabase_url,pool_pre_ping=True)
LocalSession = sessionmaker(bind=engine,autoflush=False,autocommit=False)

# DB Dependency for route injection
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()



```


##### Create a async function which listens for the changes in db

create a async function which always listens for the changes in the db of the perticular table and associate with a function of perform desired operation if changes detected

This is how the main.py file looks

`main.py`

```python
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
            lambda status, error=None: print(f"📡 Channel Status: {status}", f"| Error: {error}" if error else "")
            )
        )
        await asyncio.sleep(0.5)
        print("Real-time Event channels open successfully..")
    else:
        print("Realtime Configuration skipped due to missing project url")
  
    yield
  
    print("Clearning application resources..")


app = FastAPI(lifespan=app_lifespan)

```

in last bind the async @asynccontextmanager with the instance of the fastAPI i.e. is 'app'

`app = FastAPI(lifespance = app_lifespan)`

that it as of June13,2026 9:25PM
