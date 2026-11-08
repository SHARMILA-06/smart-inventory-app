# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import database

app = FastAPI(title="Smart Inventory API", version="1.0")

# App start agum pothu database table create agum
database.init_db()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Inventory & AI Analytics API!"}

# 1. Get all items from database
@app.get("/items/")
def get_items(db: Session = Depends(get_db)):
    items = db.query(database.ItemModel).all()
    return items

# 2. Add a new item to database
@app.post("/items/")
def create_item(name: str, quantity: int, status: str, db: Session = Depends(get_db)):
    new_item = database.ItemModel(name=name, quantity=quantity, status=status)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Item added successfully!", "item": new_item}