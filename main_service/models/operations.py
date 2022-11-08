from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum
from decimal import Decimal

class OperationKind(str, Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'

class OperationBase(BaseModel):
    date: date
    kind: OperationKind
    amount: Decimal
    description: Optional[str]

class Operation(OperationBase):
    id: int

    class Config:
        orm_mode = True

class OperationCreate(OperationBase):
    pass

class OperationUpdate(OperationBase):
    pass