import firebase_admin
from firebase_admin import credentials, firestore
import json

def init_database():
    credential = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(credential)
    database = firestore.client()
    
    return database
    
def get_database(database):
    datas = database.collection('Database').stream()
    projects = [data.to_dict() for data in datas]
    json_data = json.loads(json.dumps(projects))
    
    return json_data

def write_database(database, new_json):
    for document in database.collection('Database').list_documents():
        document.delete()
    for data in new_json:
        database.collection('Database').document(data["id"]).set(data)

# デバッグ用     
# credential = credentials.Certificate("credentials.json")
# firebase_admin.initialize_app(credential)
# database = firestore.client()
# with open("./test/dataset.json", "r") as file:
#     datas = json.load(file)
# for document in database.collection('Database').list_documents():
#     document.delete()
# for data in datas:
#     database.collection('Database').document(data["id"]).set(data)