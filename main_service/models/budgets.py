from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum
from decimal import Decimal

class Budget(BaseModel):
    id: int
    amount: float
    f1: int
    f2: int

    class Config:
        orm_mode = True