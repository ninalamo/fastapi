from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from . import crud, models, database
from .schemas import Item, ItemInDB

app = FastAPI()

# Initialize database
database.init_db()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Item
@app.post("/items/", response_model=ItemInDB)
def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = crud.create_item(db=db, item=item)
    return db_item

# Read Items
@app.get("/items/", response_model=List[ItemInDB])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_items(db=db, skip=skip, limit=limit)
    return items

# Read Item by ID
@app.get("/items/{item_id}", response_model=ItemInDB)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Update Item
@app.put("/items/{item_id}", response_model=ItemInDB)
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = crud.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Delete Item
@app.delete("/items/{item_id}", response_model=ItemInDB)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
