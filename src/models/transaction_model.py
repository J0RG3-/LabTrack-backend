from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class TransactionBase(BaseModel):
    compound_id: str
    instance_id: str
    type: Literal["use", "restock"]
    quantity: float
    unit: str
    timestamp: datetime
    user_id: int
    user_name: str
    notes: Optional[str] = None
    location: Optional[str] = None

class TransactionCreate(TransactionBase):
    id: Optional[str] = None
    original_quantity: Optional[float] = None
    new_quantity: Optional[float] = None
    compound_name: Optional[str] = None
    batch_number: Optional[str] = None

class TransactionOut(TransactionCreate):
    pass
