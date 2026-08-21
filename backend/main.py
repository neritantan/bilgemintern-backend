from fastapi import FastAPI
from pydantic import BaseModel
import random

# db baglanacak note endpointleri ile dbden veri cekilecek basit bir frontend vibe-coded
app = FastAPI()

class NoteUser(BaseModel):
    text: str

class NoteDB(BaseModel):
    note_id: int
    text: str

fruits = ["apple", "banana", "strawberry", "mango", "peach"]
notes = []
notecount = len(notes)

@app.get("/")
async def root():
    return {"fruit": random.choice(fruits)}

@app.get("/notes")
async def get_notes():
    #once dbdeki son notu sonra tum notlari return edecek
    return notes

@app.post("/notes") #POST
async def post_note(note: NoteUser):
    global notecount
    #db e son notun sonuna +1 ekleyip id olarak gonderecek aciklamayla
    noteToDB = {"note_id": len(notes),
                "text": note.text }
    
    notes.append(noteToDB)
    notecount = len(notes) # bunun global olmasi gerek
    return notes

@app.get("/notes/{note_id}")
async def get_note(note_id: int):
    return {"note_id": note_id,
            "text": "blablalbalba",
            "fruit": fruits[note_id]}

