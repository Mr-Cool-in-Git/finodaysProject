from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum
from decimal import Decimal

class User(BaseModel):
    id: int
    login: str
    password: str
    name: str
    token: str
    green_bank_id: int = None
    yellow_bank_id: int = None
    red_bank_id: int = None

    class Config:
        orm_mode = True