import os

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    message: str

CSV_FILE = "C:Users/Joanna/Dropbox/PC/Downloads/chars/chars.csv"  

if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["name", "message"])
    df.to_csv(CSV_FILE, index=False)

@app.get("/characters") 
def get_all_data():
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records")

@app.get("/characters/{name}")
def get_data(name: str):
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records")

@app.post("/characters/{name}")
def receive_data(item: Item):
    df = pd.read_csv(CSV_FILE)
    new_data = pd.DataFrame([{"name": item.name, "message": item.message}])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return {"message": "Data saved successfully", "data": item}