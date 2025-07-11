from pydantic import BaseModel, Field
from typing import Optional

class CompoundBase(BaseModel):
    name: str
    cas_number: Optional[str] = None
    threshold: float
    unit: str
    hazard_class: Optional[str] = None
    supplier: Optional[str] = None
    synonyms: Optional[str] = None
    notes: Optional[str] = None

class CompoundCreate(CompoundBase):
    id: str

class CompoundOut(BaseModel):
    id: str
    name: str
    cas_number: Optional[str]
    threshold: float
    unit: str
    hazard_class: Optional[str]
    supplier: Optional[str]
    synonyms: Optional[str]
    notes: Optional[str]


class CompoundUpdate(BaseModel):
    name: str
    cas_number: Optional[str]
    threshold: float
    unit: str
    hazard_class: Optional[str] = None
    supplier: Optional[str]
    synonyms: Optional[str]
    notes: Optional[str]

