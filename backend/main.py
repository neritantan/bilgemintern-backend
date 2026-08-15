from fastapi import FastAPI
from pydantic import BaseModel
import random

# db baglanacak note endpointleri ile dbden veri cekilecek basit bir frontend vibe-coded
app = FastAPI()

class Note(BaseModel):
    note_id: int
    note: str




@app.get("/")
async def root():
    fruits = ("apple", "banana", "strawberry", "mango")
    return {"fruit": random.choice(fruits)}

@app.get("/notes")
async def get_notes():
    #once dbdeki son notu sonra tum notlari return edecek
    return None

@app.post("/notes")
async def post_note():
    #db e son notun sonuna +1 ekleyip id olarak gonderecek aciklamayla
    return None



@app.get("/notes/{note_id}")
async def get_note(note_id: int):
    return {"note_id": note_id,
            "desc": "blablalbalba"}

