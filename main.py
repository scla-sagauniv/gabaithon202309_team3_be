from fastapi import FastAPI
from pydantic import BaseModel
import firebase

FIREBASE = firebase.init_database()

app = FastAPI()
    
@app.get("/database")
async def get_database():
    return firebase.get_database(FIREBASE)

class Idea(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    thumbnail: str | None = None
    method: str

@app.post("/idea")
async def update_idea(data: Idea):
    database = firebase.get_database(FIREBASE)
    
    if data.method == "add":
        ids = [int(idea["id"]) for idea in database]
        ids.sort()
        id = [id for id in list(range(1, ids[-1] + 2)) if id not in [int(idea["id"]) for idea in database]][0]
        database.append({"id": id, "name": data.name, "description": data.description, "category": data.category, "thumbnail": data.thumbnail})
    
    firebase.write_database(FIREBASE, database)     

class Idea(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str | None = None
    thumbnail: str | None = None
    
