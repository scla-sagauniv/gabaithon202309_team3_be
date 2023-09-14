from fastapi import FastAPI
from pydantic import BaseModel
import firebase
import json
import requests

FIREBASE = firebase.init_database()
with open("api.txt", "r") as file:
    API_KEY = file.readline().strip()

class Idea(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    thumbnail: str | None = None
    update: bool
    
class Thumbnail(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
    
@app.get("/database")
async def get_database():
    return firebase.get_database(FIREBASE)

@app.post("/update")
async def update_idea(data: Idea):
    database = firebase.get_database(FIREBASE)
    
    if data.name not in [idea["name"] for idea in database] and data.update:
        ids = [int(idea["id"]) for idea in database]
        ids.sort()
        id = [id for id in list(range(1, ids[-1] + 2)) if id not in [int(idea["id"]) for idea in database]][0]
        database.append({"id": id, "name": data.name, "description": data.description, "category": data.category, "thumbnail": data.thumbnail})
        
        firebase.write_database(FIREBASE, database)
        
        return {"result": "データが正常に受信され、処理された"}
    else:
        return {"result": "重複データが存在し、処理に失敗した"}

@app.post("/generate")
async def generate_thumbnail(data: Thumbnail):
    payload = json.dumps({"key": f"{API_KEY}",
                          "prompt": f"{data.name}, {data.description}",
                          "negative_prompt": None,
                          "width": "400",
                          "height": "400",
                          "samples": "1",
                          "num_inference_steps": "20",
                          "seed": None,
                          "guidance_scale": 10,
                          "safety_checker": "yes",
                          "multi_lingual": "yes",
                          "panorama": "no",
                          "self_attention": "no",
                          "upscale": "no",
                          "embeddings_model": None,
                          "webhook": None,
                          "track_id": None})

    url = "https://stablediffusionapi.com/api/v3/text2img"
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload)
    thumbnail_url = response.json()["output"][0]

    return {"url": thumbnail_url}