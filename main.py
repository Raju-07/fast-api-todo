from fastapi import FastAPI

app = FastAPI()

todos = {
    'id':1,
    'title':'Learn Fastapi',
}

@app.get('/')
def get_todos():
    return todos
