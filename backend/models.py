from pydantic import BaseModel
from typing import Optional


class CalendarCreate(BaseModel):
    name: str
    year: int


class CalendarClone(BaseModel):
    new_name: str
    new_year: int


class EventCreate(BaseModel):
    dia: int
    mes: str
    titulo: str
    opciones: str = ""


class EventUpdate(BaseModel):
    dia: Optional[int] = None
    mes: Optional[str] = None
    titulo: Optional[str] = None
    opciones: Optional[str] = None
