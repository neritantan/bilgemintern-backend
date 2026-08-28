from fastapi import FastAPI
from pydantic import BaseModel
import random
import json
import os

app = FastAPI()

class NoteUser(BaseModel):
    text: str

class NoteDB(BaseModel):
    note_id: int
    text: str

fruits = ["apple", "banana", "strawberry", "mango", "peach", "tomato"]

NOTES_FILE = "data/notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE) as f:
            return json.load(f)
    return []

def save_notes():
    os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)

notes = load_notes()
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
    save_notes()
    return notes

@app.get("/notes/{note_id}")
async def get_note(note_id: int):
    return {"note_id": note_id,
            "text": "blablalbalba",
            "fruit": fruits[note_id]}

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    global notecount
    notes[:] = [n for n in notes if n["note_id"] != note_id]
    notecount = len(notes)
    save_notes()
    return notes

