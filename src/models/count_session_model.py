from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime

class CountSessionBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    created_by: Optional[int] = None
    start_date: Optional[date] = None
    completed_date: Optional[date] = None
    completed: Optional[bool] = False
    counted_items: Optional[int] = 0
    total_items: Optional[int] = 0
    duration: Optional[str] = None
    notes: Optional[str] = None

    @field_validator('start_date', 'completed_date', mode='before')
    def parse_dates(cls, v):
        if isinstance(v, str):
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError(f"Fecha inválida: {v}")
        return v

class CountSessionCreate(BaseModel):
    name: str
    location: str
    description: Optional[str] = None

class CountSessionOut(CountSessionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
