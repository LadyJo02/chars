import os

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pydantic models for data validation
class Item(BaseModel):
    name: str
    message: str

class BibleVerse(BaseModel):
    verse_message: str
    chapter_verse: str

# Define CSV file paths
CSV_FILE = CSV_FILE = "C:/Users/Joanna/Dropbox/PC/Downloads/chars/chars.csv"  
BIBLE_CSV_FILE = CSV_FILE = "C:/Users/Joanna/Dropbox/PC/Downloads/chars/bible_verses.csv"

# Initialize CSV files if they don't exist
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["name", "message"])
    df.to_csv(CSV_FILE, index=False)

if not os.path.exists(BIBLE_CSV_FILE):
    df_bible = pd.DataFrame(columns=["verse_message", "chapter_verse"])
    df_bible.to_csv(BIBLE_CSV_FILE, index=False)

# --- Endpoints for Characters ---

@app.get("/characters")
def get_all_data():
    """Get all character data."""
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records")

@app.get("/characters/{name}")
def get_data(name: str):
    """Get data for a specific character by name."""
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records")

@app.post("/characters/{name}")
def receive_data(item: Item):
    """Add a new character with a name and message."""
    df = pd.read_csv(CSV_FILE)
    new_data = pd.DataFrame([{"name": item.name, "message": item.message}])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return {"message": "Data saved successfully", "data": item}

# --- Endpoints for Bible Verses ---

@app.post("/bible_verses")
def add_bible_verse(verse: BibleVerse):
    """Add a new Bible verse with message and chapter/verse."""
    df_bible = pd.read_csv(BIBLE_CSV_FILE)
    new_verse = pd.DataFrame([{"verse_message": verse.verse_message, "chapter_verse": verse.chapter_verse}])
    df_bible = pd.concat([df_bible, new_verse], ignore_index=True)
    df_bible.to_csv(BIBLE_CSV_FILE, index=False)
    return {"message": "Bible verse saved successfully", "data": verse}

@app.get("/bible_verses")
def get_all_bible_verses():
    """Get all Bible verses."""
    df_bible = pd.read_csv(BIBLE_CSV_FILE)
    return df_bible.to_dict(orient="records")