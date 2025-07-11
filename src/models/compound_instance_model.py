from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompoundInstanceBase(BaseModel):
    compound_id: str
    location: str
    batch_number: str
    quantity: float
    unit: str
    received_date: datetime
    expiry_date: datetime
    opened_date: Optional[datetime] = None
    status: str = "active"
    description: Optional[str] = None

class CompoundInstanceCreate(CompoundInstanceBase):
    id: Optional[str] = None

class CompoundInstanceOut(CompoundInstanceCreate):
    created_at: datetime
