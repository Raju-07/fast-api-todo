from datetime import date,timedelta
from fastapi import FastAPI
from todo_model import Todo,Priority
app = FastAPI()

today =date.today()

todos = [    
Todo(id=1, title="Learn FastAPI", description="Start FastAPI tutorial", priority=Priority.high,   created_at=today + timedelta(days=0)),
Todo(id=2, title="Read Pydantic", description="Read Pydantic docs",priority=Priority.medium, created_at=today + timedelta(days=1)),
Todo(id=3, title="Write tests", description="Write unit tests",priority=Priority.low,    created_at=today + timedelta(days=2)),
Todo(id=4, title="Build API", description="Create endpoints",priority=Priority.high,   created_at=today + timedelta(days=3)),
Todo(id=5, title="Add auth", description="Implement auth",priority=Priority.high,   created_at=today + timedelta(days=4)),
Todo(id=6, title="Docs", description="Document API",priority=Priority.medium, created_at=today + timedelta(days=5)),    
Todo(id=7, title="CI/CD", description="Set up CI pipeline",priority=Priority.medium, created_at=today + timedelta(days=6)),    
Todo(id=8, title="Debug", description="Fix reported bugs",priority=Priority.low,    created_at=today + timedelta(days=7)),    
Todo(id=9, title="Refactor", description="Refactor codebase",priority=Priority.medium, created_at=today + timedelta(days=8)),    
Todo(id=10, title="Optimize", description="Performance improvements",priority=Priority.low,    created_at=today + timedelta(days=9)),    
Todo(id=11, title="Deploy", description="Deploy to staging",priority=Priority.high,   created_at=today + timedelta(days=10)),    
Todo(id=12, title="Monitor", description="Add monitoring",priority=Priority.medium, created_at=today + timedelta(days=11)),    
Todo(id=13, title="Feedback", description="Collect user feedback",priority=Priority.low,    created_at=today + timedelta(days=12)),    
Todo(id=14, title="Bugfix", description="Critical bugfix",priority=Priority.high,   created_at=today + timedelta(days=13)),    
Todo(id=15, title="Upgrade deps", description="Update dependencies",priority=Priority.medium, created_at=today + timedelta(days=14)),    
Todo(id=16, title="Cleanup", description="Remove unused code",priority=Priority.low,    created_at=today + timedelta(days=15)),    
Todo(id=17, title="Analytics", description="Add analytics",priority=Priority.medium, created_at=today + timedelta(days=16)),    
Todo(id=18, title="UX", description="Improve UX",priority=Priority.low,    created_at=today + timedelta(days=17)),    
Todo(id=19, title="Scale", description="Horizontal scaling",priority=Priority.high,   created_at=today + timedelta(days=18)),    
Todo(id=20, title="Release", description="Prepare release notes",priority=Priority.medium, created_at=today + timedelta(days=19)),]

@app.get('/')
def get_todos():
    return todos

@app.get("/todos/{id}")
def get_todo_by_id(id:int):
    for todo in todos:
        if todo.id == id:
            return todo
    return "Not Found"
