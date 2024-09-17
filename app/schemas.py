from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    done: bool = False

class ItemInDB(Item):
    id: int
